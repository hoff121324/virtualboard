QUnit.module( "QueueTest", function(hooks){

    hooks.beforeEach(function (assert){

    });

    hooks.afterEach(function(assert){
        VBoard.board.clearBoard();
    });

    QUnit.test("Testing Generating Pieces", function(assert){

        assert.notEqual(VBoard.users.getLocal(), VBoard.users.getNone(), "We expect the local user to exist");
        
    });

});