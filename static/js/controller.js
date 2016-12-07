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
    $scope.allReqs = [];
    
    $scope.requestSent = [];
    $scope.requestReceived = [];
    
    socket.on('connect', function(){
        console.log('Connected from controller');
        socket.emit('isRecvr');
    });
    
    $scope.search = function search() {
        $scope.found2 = [];

        console.log("Searching for " + $scope.searchFor);
        socket.emit('sSearch', $scope.searchFor);
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
                $scope.found2[i] = {'mealType':$scope.found[i][0], 'name': $scope.found[i][3], 'timeOne': $scope.found[i][1], 'timeTwo':$scope.found[i][2], 'id': $scope.found[i][4]};
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
    };
    
    $scope.sendReq = function sendReq(){
        console.log($scope.name + ' - ' + $scope.avId);
        var tmp = {'avId': $scope.avId};
        socket.emit('sendReq', tmp);
    };

    socket.on('allAvailability', function(av){
        var i;
        for (i =0; i< av.length; i++){
                console.log("~ " + av[i]); 
                var tmp = {'name': av[i][3],'mealType': av[i][0],'timeOne': av[i][1],'timeTwo': av[i][2],'id': av[i][4]};
                $scope.allGivers[i] = tmp;
        }
        
        $scope.$apply();
    });
    
    socket.on('getSent', function(tmp){
        console.log('getSent');
        var i;
        for(i = 0; i < tmp.length; i++){
            console.log(tmp[i]);
            var temp = {'username':tmp[i][4],'email':tmp[i][5], 'mealtype':tmp[i][1], 'starttime':tmp[i][2], 'endtime':tmp[i][3]};
            $scope.userRequests[i] = temp;
            console.log($scope.userRequests[i]['mealtype']);
        }
        
        $scope.$apply();
    });
    
    socket.on('getReceived', function(tmp){
        console.log('getReceived');
        var i;
        for(i = 0; i < tmp.length; i++){
            var temp = {'username':tmp[i][6],'email':tmp[i][5], 'mealtype':tmp[i][1], 'starttime':tmp[i][2], 'endtime':tmp[i][3]};
            
            $scope.allReqs[i] = temp;
            console.log($scope.allReqs[i]);
        }

        $scope.$apply();
    });
});