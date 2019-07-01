$("#add-problem-button").click(function(){
	$.post(
		'/api/add_problem',
		{'content': $('#add-problem-textarea').val()}
	).done(function(){
		location.reload();
	});
});

$('#button-download-user-set').click(function(){
	$.post(
		'/api/download_user_set'
	).done(function(){
		location.reload();
	});
})

$('#button-download-problem-name').click(function(){
	$.post(
		'/api/download_problem_name'
	).done(function(){
		location.reload();
	});
})

function delete_problem(index) {
	$.post(
		'/api/delete_problem',
		{'index': index}
	).done(function(){
		location.reload();
	});
}