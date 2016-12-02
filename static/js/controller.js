var App = angular.module('App', []);

App.controller('AppController', function($scope){
    var socket = io.connect('https://' + document.domain + ':' + location.port);
    
    $scope.found = [];
    $scope.found2 = [];
    
    socket.on('connect', function(){
        console.log('Connected from controller'); 
    });
    
    $scope.search = function search() {
        $scope.found2 = [];
        //clear();
        
        console.log("Searching for " + $scope.searchFor);
        socket.emit('sSearch', $scope.searchFor);
    
        //$scope.$apply();
    };
    
    $scope.clear = function clear(){
        $scope.found2 = [];
        $scope.$apply();
    };
    
    socket.on('found', function(res,srch_type){
        
        $scope.found = res;
        var i;
    
        if ($scope.found[0].length > 2){
            for (i =0; i< $scope.found.length; i++){
                $scope.found2[i] = $scope.found[i][3] + " is available for " + $scope.found[i][0] + " from " + $scope.found[i][1] + " - " + $scope.found[i][2];
                console.log("~ " + $scope.found[i][3] + " is available from " + $scope.found[i][1] + " - " + $scope.found[i][2]); 
            }
        } else {
            for (i =0; i< $scope.found.length; i++){
                $scope.found2[i] = "~ " + $scope.found[i][1];
                console.log("~ " + $scope.found[i][1]); 
            }
        }
        
        $scope.$apply();
        
    });
    
});