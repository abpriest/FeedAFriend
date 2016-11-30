var App = angular.module('App', []);

App.controller('AppController', function($scope){
    var socket = io.connect('https://' + document.domain + ':' + location.port);
    
    $scope.found = [];
    
    socket.on('connect', function(){
       console.log('Connected from controller'); 
    });
    
    $scope.search = function search() {
        console.log("Searching for " + $scope.searchFor);
        socket.emit('sSearch', $scope.searchFor);
        
    };
    
    socket.on('found', function(res,srch_type){
       $scope.found = res;
       var i;
       if ($scope.found[0].length > 2){
           for (i =0; i< $scope.found.length; i++){
        console.log("~ " + $scope.found[i][3] + " is available from " + $scope.found[i][1] + " - " + $scope.found[i][2]); 
    
       }
       } else {
       
       
       for (i =0; i< $scope.found.length; i++){
        console.log("~ " + $scope.found[i][1]); 
    
       }
       }
     });
    
});