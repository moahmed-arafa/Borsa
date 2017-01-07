/**
 * Created by fantom on 12/7/16.
 */
(function () {

  'use strict';

  angular.module('WordcountApp', [])

  .controller('WordcountController', ['$scope', '$log',
    function($scope, $log) {
    $scope.getResults = function() {
      $log.log("test");
         // fire the API request
    $http.post('/uploadCatsCSV', {"url": userInput}).
      success(function(results) {
        $log.log(results);
      }).
      error(function(error) {
        $log.log(error);
      });
    };
  }

  ]);

}());