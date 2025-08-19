from django.db import models
from django.utils.text import slugify


class SEOMixin(models.Model):
    """
    Simplified SEO mixin for all content models
    Provides essential SEO fields with automatic fallbacks
    """
    
    # Core SEO fields
    meta_title = models.CharField(
        max_length=60, 
        blank=True,
        help_text="SEO title (max 60 chars). Leave blank to auto-generate from title."
    )
    meta_description = models.CharField(
        max_length=160, 
        blank=True,
        help_text="SEO description (max 160 chars). Leave blank to auto-generate."
    )
    meta_keywords = models.CharField(
        max_length=255, 
        blank=True,
        help_text="Comma-separated keywords for SEO"
    )
    
    # Open Graph fields
    og_title = models.CharField(
        max_length=60, 
        blank=True,
        help_text="Open Graph title. Leave blank to use meta_title."
    )
    og_description = models.CharField(
        max_length=160, 
        blank=True,
        help_text="Open Graph description. Leave blank to use meta_description."
    )
    
    class Meta:
        abstract = True
    
    def get_meta_title(self):
        """Get SEO title with fallback to main title"""
        if self.meta_title:
            return self.meta_title
        # Fallback to main title field (assumes model has 'title' or 'name')
        if hasattr(self, 'title'):
            return self.title[:60]
        elif hasattr(self, 'name'):
            return self.name[:60]
        return "Skyline Ghana Constructions"
    
    def get_meta_description(self):
        """Get SEO description with fallback"""
        if self.meta_description:
            return self.meta_description
        # Fallback to description or short_description
        if hasattr(self, 'description') and self.description:
            return self.description[:160]
        elif hasattr(self, 'short_description') and self.short_description:
            return self.short_description[:160]
        return "Professional construction services in Ghana - Building Dreams, Creating Futures"
    
    def get_meta_keywords(self):
        """Get SEO keywords with fallback"""
        if self.meta_keywords:
            return self.meta_keywords
        # Auto-generate basic keywords
        keywords = ["construction", "Ghana", "building"]
        if hasattr(self, 'category') and self.category:
            if hasattr(self.category, 'name'):
                keywords.append(self.category.name.lower())
        if hasattr(self, 'title'):
            # Add title words as keywords
            title_words = [word.lower() for word in self.title.split() if len(word) > 3]
            keywords.extend(title_words[:3])  # Limit to 3 words
        return ", ".join(keywords)
    
    def get_og_title(self):
        """Get Open Graph title"""
        return self.og_title or self.get_meta_title()
    
    def get_og_description(self):
        """Get Open Graph description"""
        return self.og_description or self.get_meta_description()


class TimestampMixin(models.Model):
    """
    Simplified timestamp mixin
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class SlugMixin(models.Model):
    """
    Simplified slug mixin with auto-generation
    """
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Auto-generate slug from title or name
            if hasattr(self, 'title'):
                self.slug = slugify(self.title)
            elif hasattr(self, 'name'):
                self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class StatusMixin(models.Model):
    """
    Common status fields for content
    """
    is_active = models.BooleanField(default=True, help_text="Show on website")
    is_featured = models.BooleanField(default=False, help_text="Feature prominently")
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    
    class Meta:
        abstract = True
        ordering = ['order', 'id']
