var App = angular.module('App', []);

App.controller('AppController', function($scope){
    var socket = io.connect('https://' + document.domain + ':' + location.port);
    
    $scope.found = [];
    $scope.found2 = [];
    $scope.name = '';
    $scope.mealType = '';
    $scope.timeOne = '';
    $scope.timeTwo = '';
    $scope.avId = '';
    $scope.userRequests = [];
    $scope.allGivers = [];
    
    $scope.requestSent = [];
    $scope.requestReceived = [];
    
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
        console.log($scope.name + ' - ' + $scope.avId);
        var tmp = {'avId': $scope.avId};
        socket.emit('sendReq', tmp);
    };

    socket.on('allAvailability', function(av){
        //console.log('Hello');
        //console.log(av[0]);
        var i;
        for (i =0; i< av.length; i++){
                //$scope.found2[i] = "~ " + $scope.found[i][1];
                console.log("~ " + av[i]); 
                var tmp = {'name': av[i][3],'mealType': av[i][0],'timeOne': av[i][1],'timeTwo': av[i][2],'id': av[i][4]};
                $scope.allGivers[i] = tmp;
        }
        
        $scope.$apply();
        
    });
    
    socket.on('getSent', function(tmp){
        console.log('getSent')
        $scope.requestSent.push(tmp);
        $scope.$apply();
    });
    
    socket.on('getReceived', function(tmp){
        console.log('getReceived')
        $scope.requestReceived.push(tmp);
        $scope.$apply();
    });
});