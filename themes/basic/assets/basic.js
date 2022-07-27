const urlSearchParams = new URLSearchParams(location.search);
const paramKey = "expandedpolicy";
let toggledOnByDefault = [];

function toggle(event) {
	const classname = "screenreader-only";
	let bodyId = event.target.getAttribute("x-toggle-data") + "-body";
	
	if (event.target.checked == false) {
		// hide for visual people
		// don't hide for users of assistive technologies as they use alternative methods of navigating a website
		document.getElementById(bodyId).classList.add(classname);
	} else {
		// show for visual people
		// don't change anything for users of assistive technologies as they use alternative methods of navigating a website
		document.getElementById(bodyId).classList.remove(classname);
		// for all others including users of assistive technologies
		if (event.issuedByQueryString == undefined) {
			document.getElementById(bodyId).focus();
			document.getElementById(bodyId).scrollIntoView();
		}
	}
}

for (let elem of document.getElementsByTagName("input")) {
	if (elem.type != "checkbox") {
		continue;
	}
	elem.addEventListener("click", toggle);
}

if (urlSearchParams.has(paramKey)) {
	toggledOnByDefault.push(...urlSearchParams.get(paramKey).split(","));
}

for (let item of toggledOnByDefault) {
	document.getElementById(item + "-heading").checked = true;
	let e = new Object();
	e.issuedByQueryString = true;
	e.target = document.getElementById(item + "-heading");
	toggle(e);
}