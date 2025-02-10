JAZZMIN_SETTINGS = {
    "site_title": "My E-commerce Admin",
    "site_header": "E-commerce Dashboard",
    "site_brand": "E-commerce Admin",
    "welcome_sign": "Welcome to the E-commerce Admin Panel!",
    "copyright": "E-commerce",
    "search_model": "product.Product",  # Enable global search on the Product model
    "user_avatar": None,  # Customize if you have user profile pictures

    # Custom top menu links
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Products", "url": "/admin/product/product/", "permissions": ["product.view_product"]},
    ],

    # Apps displayed in the side menu
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["auth", "product", "order"],

    # Custom icons for apps/models (using FontAwesome icons)
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "product.Product": "fas fa-box",
        "order.Order": "fas fa-shopping-cart",
    },

    # Custom related models to be shown in detail views
    "related_modal_active": True,

    # Customize the appearance
    "custom_css": None,
    "custom_js": None,
    "theme": "lux",  # Available themes: darkly, cyborg, flatly, lumen, lux, etc.
}

# Optional: Jazzmin UI Tweaks
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-dark bg-primary",
    "no_navbar_border": True,
    "sidebar_nav_small_text": True,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "theme": "lux",
    "dark_mode_theme": None,
}
