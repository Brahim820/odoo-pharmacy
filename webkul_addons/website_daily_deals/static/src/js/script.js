$(document).ready(function(){

	$("#slideshow li img")
	$("#slideshow #7").show("fade", 500);
	var sc = $("#slideshow li img").size();
	var count = 14;
	function slideLeft(count, sc){
		$("#slideshow #"+count).hide("slide", {direction:'left'}, 400, function(){
			count = increaseCount(count, sc)
			$("#slideshow #"+count).show("slide", {direction:'right'}, 400);
		});
	}
	
	function slideRight(count, sc){
		$("#slideshow #"+count).hide("slide", {direction:'right'}, 400, function(){
			count = decreaseCount(count, sc);
			$("#slideshow #"+count).show("slide", {direction:'left'}, 400);
		});
	}
	
	$(".prev").on("click", function(){
		slideLeft(count, sc);
		count = increaseCount(count, sc)
		console.log(count);
	});
	
	$(".next").on("click", function(){
		slideRight(count, sc);
		count = decreaseCount(count, sc);
		console.log(count);
	});
	
	function increaseCount(count, sc){
		if (count == sc)
			count = 1
		else
			count = count + 1;
		
		return count;
	}
	
	function decreaseCount(count, sc){
		if (count == 1)
			count = sc;
		else
			count = count - 1;
		
		return count;
	}
});