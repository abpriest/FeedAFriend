var App = angular.module('App', []);

App.controller('AppController', function($scope){
    var socket = io.connect('https://' + document.domain + ':' + location.port);
    
    socket.on('connect', function(){
       console.log('Connected from controller'); 
    });
    
    $scope.search = function search() {
          console.log("Searching for " + $scope.searchFor);
          
        };
    
});