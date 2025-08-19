import json
import os
import tempfile
import zipfile
from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import transaction
from django.conf import settings
from datetime import datetime


class Command(BaseCommand):
    help = 'Restore data from a backup (works across different database engines)'

    def add_arguments(self, parser):
        parser.add_argument(
            'backup_path',
            type=str,
            help='Path to backup directory or zip file'
        )
        parser.add_argument(
            '--include-media',
            action='store_true',
            help='Restore media files from backup',
        )
        parser.add_argument(
            '--clear-existing',
            action='store_true',
            help='Clear existing data before restore (DANGEROUS!)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be restored without actually doing it',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Skip confirmation prompts (for API usage)',
        )

    def handle(self, *args, **options):
        backup_path = options['backup_path']
        
        self.stdout.write('Starting data restore...')
        
        # Handle zip files
        temp_dir = None
        if backup_path.endswith('.zip'):
            temp_dir = tempfile.mkdtemp()
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extractall(temp_dir)
            backup_path = temp_dir
        
        try:
            # Validate backup
            if not self.validate_backup(backup_path):
                self.stdout.write(
                    self.style.ERROR('Invalid backup format or missing files')
                )
                return
            
            # Show backup info
            self.show_backup_info(backup_path)
            
            if options['dry_run']:
                self.stdout.write('DRY RUN - No changes will be made')
                self.show_restore_plan(backup_path)
                return
            
            # Confirm restore (skip if force flag is used)
            if not options['force']:
                if not options['clear_existing']:
                    confirm = input('This will add data to your database. Continue? (y/N): ')
                    if confirm.lower() != 'y':
                        self.stdout.write('Restore cancelled')
                        return
                else:
                    confirm = input('WARNING: This will CLEAR ALL EXISTING DATA and restore from backup. Are you sure? (type "yes" to confirm): ')
                    if confirm != 'yes':
                        self.stdout.write('Restore cancelled')
                        return
            
            # Perform restore
            with transaction.atomic():
                if options['clear_existing']:
                    self.clear_existing_data()
                
                self.restore_database_data(backup_path)
                
                if options['include_media']:
                    self.restore_media_files(backup_path)
            
            self.stdout.write(
                self.style.SUCCESS('Restore completed successfully!')
            )
            
        finally:
            # Clean up temporary directory
            if temp_dir and os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir)

    def validate_backup(self, backup_path):
        """Validate backup structure"""
        if not os.path.exists(backup_path):
            return False
        
        # Check for required files/directories
        data_dir = os.path.join(backup_path, 'data')
        metadata_file = os.path.join(backup_path, 'backup_metadata.json')
        
        return os.path.exists(data_dir) and os.path.exists(metadata_file)

    def show_backup_info(self, backup_path):
        """Show backup information"""
        metadata_file = os.path.join(backup_path, 'backup_metadata.json')
        
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            self.stdout.write('\nBackup Information:')
            self.stdout.write(f'  Date: {metadata.get("backup_date", "Unknown")}')
            self.stdout.write(f'  Django Version: {metadata.get("django_version", "Unknown")}')
            self.stdout.write(f'  Database Engine: {metadata.get("database_engine", "Unknown")}')
            self.stdout.write(f'  Apps: {", ".join(metadata.get("apps_included", []))}')
            self.stdout.write('')

    def show_restore_plan(self, backup_path):
        """Show what would be restored"""
        data_dir = os.path.join(backup_path, 'data')
        
        self.stdout.write('Restore Plan:')
        for file in os.listdir(data_dir):
            if file.endswith('.json'):
                app_name = file[:-5]  # Remove .json extension
                file_path = os.path.join(data_dir, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    app_data = json.load(f)
                
                self.stdout.write(f'  App: {app_name}')
                for model_name, records in app_data.items():
                    self.stdout.write(f'    {model_name}: {len(records)} records')

    def clear_existing_data(self):
        """Clear existing data from all app models"""
        self.stdout.write('Clearing existing data...')
        
        # Get all models in reverse dependency order
        all_models = []
        for app_config in apps.get_app_configs():
            if app_config.name.startswith('django.'):
                continue
            all_models.extend(app_config.get_models())
        
        # Clear models in reverse order to handle foreign key constraints
        for model in reversed(all_models):
            count = model.objects.count()
            if count > 0:
                model.objects.all().delete()
                self.stdout.write(f'  Cleared {count} {model._meta.model_name} records')

    def restore_database_data(self, backup_path):
        """Restore database data from backup"""
        self.stdout.write('Restoring database data...')
        
        data_dir = os.path.join(backup_path, 'data')
        
        # Process apps in dependency order
        app_order = self.get_app_dependency_order()
        
        for app_name in app_order:
            file_path = os.path.join(data_dir, f'{app_name}.json')
            if os.path.exists(file_path):
                self.restore_app_data(app_name, file_path)

    def get_app_dependency_order(self):
        """Get apps in dependency order"""
        # Basic dependency order - customize as needed
        return ['core', 'accounts', 'services', 'projects', 'blog', 'contact', 'dashboard']

    def restore_app_data(self, app_name, file_path):
        """Restore data for a specific app"""
        self.stdout.write(f'  Restoring {app_name} data...')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            app_data = json.load(f)
        
        for model_name, records in app_data.items():
            try:
                # Get the model class
                model = apps.get_model(app_name, model_name)
                
                # Restore records
                restored_count = 0
                for record_data in records:
                    fields = record_data['fields']
                    pk = record_data['pk']
                    
                    # Handle foreign keys and many-to-many fields
                    fields = self.process_fields(model, fields)
                    
                    # Create or update record
                    obj, created = model.objects.update_or_create(
                        pk=pk,
                        defaults=fields
                    )
                    if created:
                        restored_count += 1
                
                self.stdout.write(f'    Restored {restored_count} {model_name} records')
                
            except Exception as e:
                self.stdout.write(f'    Error restoring {model_name}: {str(e)}')

    def process_fields(self, model, fields):
        """Process fields to handle foreign keys and special field types"""
        processed_fields = {}
        
        for field_name, value in fields.items():
            try:
                field = model._meta.get_field(field_name)
                
                # Handle foreign keys
                if hasattr(field, 'related_model') and value:
                    # For foreign keys, the value should be the primary key
                    processed_fields[field_name] = value
                else:
                    processed_fields[field_name] = value
                    
            except Exception:
                # If field doesn't exist or other error, skip it
                continue
        
        return processed_fields

    def restore_media_files(self, backup_path):
        """Restore media files from backup"""
        self.stdout.write('Restoring media files...')
        
        media_backup_path = os.path.join(backup_path, 'media')
        
        if os.path.exists(media_backup_path):
            media_root = getattr(settings, 'MEDIA_ROOT', None)
            if media_root:
                import shutil
                
                # Create media root if it doesn't exist
                os.makedirs(media_root, exist_ok=True)
                
                # Copy files
                for root, dirs, files in os.walk(media_backup_path):
                    for file in files:
                        source_path = os.path.join(root, file)
                        relative_path = os.path.relpath(source_path, media_backup_path)
                        dest_path = os.path.join(media_root, relative_path)
                        
                        # Create directory if it doesn't exist
                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                        shutil.copy2(source_path, dest_path)
                
                self.stdout.write(f'  Media files restored to {media_root}')
            else:
                self.stdout.write('  No MEDIA_ROOT configured, skipping media restore')
        else:
            self.stdout.write('  No media files found in backup')
