
# jazzmin.py

JAZZMIN_SETTINGS = {
    # Branding
    "site_title": "House Of Nepal Admin",
    "site_header": "House Of Nepal",
    "site_brand": "House Of Nepal",
    "welcome_sign": "Welcome to the House Of Nepal",
    "copyright": "© 2025 House Of Nepal",
    "search_model": "products.Product",
    "show_ui_builder":True,

    # Top menu links
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"app": "products"},
        {"name": "Support", "url": "https://support.moredealsclub.com", "new_window": True},
    ],

    # Applications to display in the sidebar
    "apps_icons": {
        "auth": "fas fa-users-cog",
        "products": "fas fa-product-hunt",
        "carts": "fas fa-shopping-cart",
        "reviews": "fas fa-star",
        "orders": "fas fa-shopping-basket",
        "meta": "fas fa-tags",
        "newsletter": "fas fa-envelope",

        "users": "fas fa-user",
    },

    "icons": {
        "accounts.EmailAddress": "fas fa-envelope",
        "sites.Sites": "fas fa-globe",
        "auth.Group": "fas fa-users",
        "auth.User": "fas fa-user",
        "products.Product": "fa-brands fa-product-hunt",
        "products.Brand": "fa-solid fa-copyright",
        "products.Category": "fas fa-list",
        "carts.Cart": "fas fa-shopping-cart",
        "carts.CartItem": "fas fa-shopping-cart",
        "reviews.Review": "fas fa-star",
        "orders.Order": "fa-solid fa-truck-fast",
        "orders.OrderItem": "fas fa-shopping-basket",
        "newsletter.NewsLetter": "fas fa-envelope",
        "users.CustomUser": "fas fa-user",
    },

    # UI Customizations
    "show_sidebar": True,
    "navigation_expanded": True,
    "custom_css": None,
    "custom_js": None,
    "related_modal_active": True,
    "use_google_fonts_cdn": True,
    "changeform_format":"horizantal_tabs",

    # Footer
    "footer_text": "© 2025 MoreLiving. All rights reserved.",

    # Custom icons for apps and models
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": True,
    "footer_small_text": True,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "sidebar_disable_expand": False,
    "sidebar_auto_collapse": True,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": True,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "changeform_format": "horizontal_tabs", 
    "form_submit_sticky": False,
    "form_inline_expand_width": True,
    "inline_stacked_controls": False,
    "actions_sticky_top": True
}