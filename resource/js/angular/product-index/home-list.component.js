// Define the `homeList` module
angular.module('homeList').component('homeList', {
    templateUrl: "http://127.0.0.1:8080/static/templates/shopping/home/home_index.template.html",
    controller: function HomeListController($http) {
        var self = this;
        initSliceItem();
        self.hostName = "http://127.0.0.1:8080";
        $http.get(feature_item_url).then(function(response){
            console.log(response.data);
            self.featureProducts = response.data;
        });
    }
});

function initSliceItem(){
    jQuery("#feartured-product-slider .slider-items").owlCarousel({
            items: 4,
            itemsDesktop: [1250, 4],
            itemsDesktopSmall: [980, 3],
            itemsTablet: [640, 2],
            itemsMobile: [360, 1],
            navigation: !0,
            navigationText: ['<a class="flex-prev"></a>', '<a class="flex-next"></a>'],
            slideSpeed: 500,
            pagination: !1,
            autoPlay: false
    })
}

