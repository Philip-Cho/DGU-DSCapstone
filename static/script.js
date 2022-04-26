$(function(){
	var controller = new ScrollMagic.Controller();
	var wipeAnimation = new TimelineMax();
		wipeAnimation.fromTo('.two', 1, {x:'-100%'}, {x:'0%'})
					.fromTo('.three', 1, {y:'-100%'},{y:'0%'})
					.fromTo('.four', 1, {x:'100%'}, {x:'0%'});
	
	var scene = new ScrollMagic.Scene({
		triggerElement: '.wrap',
		triggerHook: 'onLeave',
		duration: '500%'

	})
	.setPin('.wrap')
	.setTween(wipeAnimation)
	.addTo(controller)
	.addIndicators();										
});
