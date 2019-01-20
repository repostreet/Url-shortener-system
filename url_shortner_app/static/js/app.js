var protocol = 'http://'
var hostname = protocol + window.location.host
var application = angular.module('pocapp', [])

application.config(function($interpolateProvider, $httpProvider){         
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
});


application.controller('urlSubmitController', function($scope, $http) {
	var submitted_url = hostname + '/shorten-url/'

    $scope.postUrl = function() {
    	var data = {'url': $scope.full_url}

    	$http({
            url: submitted_url,
            method: 'POST',
            data: data

    	}).then(function(response){
            var res = response.data;
            $scope.message = res['message'];

    	}).catch(function(err){
    		var res = err.data;
    		$scope.message = res['message'];

    	});

    }
});

application.controller('listUrl', function($scope, $http) {
	var list_short_api = hostname + '/shortend-urls/'

    $http.get(list_short_api)
    .then(function(response){
    	$scope.all_short_urls = response.data;
    	console.log($scope.all_short_urls);

    }).catch(function(err){
        $scope.list_error_message = err.data['message']

    });
});

// var postUrl = function($http, $scope) {
//     console.log($scope.full_url);
// }