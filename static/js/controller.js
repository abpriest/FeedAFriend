var App = angular.module('App', []);

App.controller('AppController', function($scope){
    var socket = io.connect('https://' + document.domain + ':' + location.port);
    
    $scope.found = [];
    $scope.found2 = [];
    $scope.name = '';
    $scope.mealType = '';
    $scope.timeOne = '';
    $scope.timeTwo = '';
<<<<<<< HEAD
    $scope.req = [];
=======
    $scope.avId = '';
    $scope.userRequests = [];
    $scope.allGivers = [];
>>>>>>> be1ac75977c05f597e3dee593fc80484017e48ee
    
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
                $scope.found2[i] = {'mealType':$scope.found[i][0], 'name': $scope.found[i][3], 'timeOne': $scope.found[i][1], 'timeTwo':$scope.found[i][2], 'id': $scope.found[i][4]};//$scope.found[i][3] + " is available for " + $scope.found[i][0] + " from " + $scope.found[i][1] + " - " + $scope.found[i][2];
                console.log("~ " + $scope.found[i][3] + " is available from " + $scope.found[i][1] + " - " + $scope.found[i][2] + " ID = " + $scope.found[i][4]); 
            }
        } else {
            for (i =0; i< $scope.found.length; i++){
                $scope.found2[i] = "~ " + $scope.found[i][1];
                console.log("~ " + $scope.found[i][1]); 
            }
        }
        
        $scope.$apply();
        
    });
    
    $scope.request = function request(info){
        console.log(info);
        $scope.name = info['name'];
        $scope.timeOne = info['timeOne'];
        $scope.timeTwo = info['timeTwo'];
        $scope.mealType = info['mealType'];
        $scope.avId = info['id'];
        //$scope.$apply();
    };
    
    $scope.sendReq = function sendReq(){
<<<<<<< HEAD
        console.log($scope.name + ' - ' + $scope.mealType);
=======
        console.log($scope.name + ' - ' + $scope.avId);
        var tmp = {'avId': $scope.avId};
        socket.emit('sendReq', tmp);
>>>>>>> be1ac75977c05f597e3dee593fc80484017e48ee
    };
    
});