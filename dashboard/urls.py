from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Dashboard home
    path('', views.DashboardHomeView.as_view(), name='home'),
    path('login/', views.DashboardLoginView.as_view(), name='login'),
    path('logout/', views.DashboardLogoutView.as_view(), name='logout'),

    # Project management
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='project_edit'),
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
    path('projects/<int:pk>/images/', views.ProjectImageManageView.as_view(), name='project_images'),

    # Project categories
    path('projects/categories/', views.ProjectCategoryListView.as_view(), name='project_category_list'),
    path('projects/categories/create/', views.ProjectCategoryCreateView.as_view(), name='project_category_create'),
    path('projects/categories/<int:pk>/edit/', views.ProjectCategoryUpdateView.as_view(), name='project_category_edit'),
    path('projects/categories/<int:pk>/delete/', views.ProjectCategoryDeleteView.as_view(), name='project_category_delete'),

    # Service management
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/create/', views.ServiceCreateView.as_view(), name='service_create'),
    path('services/<int:pk>/edit/', views.ServiceUpdateView.as_view(), name='service_edit'),
    path('services/<int:pk>/toggle/', views.ServiceToggleActiveView.as_view(), name='service_toggle'),
    path('services/<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='service_delete'),

    # Service categories
    path('services/categories/', views.ServiceCategoryListView.as_view(), name='service_category_list'),
    path('services/categories/create/', views.ServiceCategoryCreateView.as_view(), name='service_category_create'),
    path('services/categories/<int:pk>/edit/', views.ServiceCategoryUpdateView.as_view(), name='service_category_edit'),

    # Inquiry management
    path('inquiries/', views.InquiryListView.as_view(), name='inquiry_list'),

    # Career management
    path('careers/', views.CareerListView.as_view(), name='career_list'),
    path('careers/create/', views.CareerCreateView.as_view(), name='career_create'),
    path('careers/<int:pk>/update/', views.CareerUpdateView.as_view(), name='career_update'),
    path('careers/<int:pk>/delete/', views.CareerDeleteView.as_view(), name='career_delete'),

    # Testimonials
    path('testimonials/', views.TestimonialListView.as_view(), name='testimonial_list'),
    path('testimonials/create/', views.TestimonialCreateView.as_view(), name='testimonial_create'),
    path('testimonials/<int:pk>/edit/', views.TestimonialUpdateView.as_view(), name='testimonial_edit'),
    path('testimonials/<int:pk>/delete/', views.TestimonialDeleteView.as_view(), name='testimonial_delete'),

    # Blog
    path('blog/', views.BlogListView.as_view(), name='blog_list'),
    path('blog/create/', views.BlogCreateView.as_view(), name='blog_create'),
    path('blog/<int:pk>/edit/', views.BlogUpdateView.as_view(), name='blog_edit'),
    path('blog/<int:pk>/delete/', views.BlogDeleteView.as_view(), name='blog_delete'),

    # Homepage Carousel Images
    path('homepage-carousel/', views.HomepageCarouselListView.as_view(), name='homepage_carousel_list'),
    path('homepage-carousel/create/', views.HomepageCarouselCreateView.as_view(), name='homepage_carousel_create'),
    path('homepage-carousel/<int:pk>/edit/', views.HomepageCarouselUpdateView.as_view(), name='homepage_carousel_edit'),
    path('homepage-carousel/<int:pk>/delete/', views.HomepageCarouselDeleteView.as_view(), name='homepage_carousel_delete'),

    # Analytics & Settings
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('settings/backup/', views.CreateBackupView.as_view(), name='create_backup'),
    path('settings/restore/', views.RestoreBackupView.as_view(), name='restore_backup'),

    # Backup Management API
    path('api/backup/', views.AdminBackupAPIView.as_view(), name='admin_backup_api'),
    path('api/restore/', views.AdminRestoreAPIView.as_view(), name='admin_restore_api'),
    path('api/backup-history/', views.AdminBackupHistoryAPIView.as_view(), name='admin_backup_history_api'),
    path('api/download-backup/', views.AdminDownloadBackupAPIView.as_view(), name='admin_download_backup_api'),
    path('api/delete-backup/', views.AdminDeleteBackupAPIView.as_view(), name='admin_delete_backup_api'),

    # Service Page Images
    path('service-images/', views.ServicePageImageListView.as_view(), name='service_image_list'),
    path('service-images/create/', views.ServicePageImageCreateView.as_view(), name='service_image_create'),
    path('service-images/<int:pk>/edit/', views.ServicePageImageUpdateView.as_view(), name='service_image_edit'),
    path('service-images/<int:pk>/delete/', views.ServicePageImageDeleteView.as_view(), name='service_image_delete'),

    # User management
    path('users/', views.UsersListView.as_view(), name='users'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),

    # Activity logs
    path('activity/', views.ActivityLogListView.as_view(), name='activity'),

    # Notifications (simple)
    path('notifications/', views.NotificationsView.as_view(), name='notifications'),
]
