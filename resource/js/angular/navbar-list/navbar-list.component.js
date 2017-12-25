// Register `catalogList` component, along with its associated controller and template

angular.module('navbarList').component('navbarList', {
    templateUrl: navbar_template_url,
    controller: function CatalogListController($http) {
        var self = this;
        $http.get(catalog_menu_url).then(function(response) {
            self.catalogs = response.data;
        });
    }
});

function initCalogMenu() {
    /*
    jQuery(document).mouseup(function (e) {
        var container = jQuery(".mega-menu-title");

        // if the target of the click isn't the container nor a descendant of the container
        if (!container.is(e.target) && container.has(e.target).length === 0) {
            jQuery('.mega-menu-category').slideUp();
        }
    });
    */
    jQuery('.mega-menu-title').on('click', function () {
        if (jQuery('.mega-menu-category').is(':visible')) {
            jQuery('.mega-menu-category').slideUp();
        } else {
            jQuery('.mega-menu-category').slideDown();
        }
    });

    jQuery('.mega-menu-category .nav > li').hover(function () {
        jQuery(this).addClass("active");
        jQuery(this).find('.popup').stop(true, true).fadeIn('slow');
    }, function () {
        jQuery(this).removeClass("active");
        jQuery(this).find('.popup').stop(true, true).fadeOut('slow');
    });
}