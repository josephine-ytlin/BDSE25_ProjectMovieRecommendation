function onlyOneCheckBox() {
	let checkboxgroup = document.getElementById("checkboxgroup").getElementsByTagName("input");
	let limit = 1;
	for (let i = 0; i < checkboxgroup.length; i++) {
		checkboxgroup[i].onclick = function() {
			let checkedcount = 0;
				for (let i = 0; i < checkboxgroup.length; i++) {
				checkedcount += (checkboxgroup[i].checked) ? 1 : 0;
			}
			if (checkedcount > limit) {
				console.log("You can select maximum of " + limit + " checkbox.");
				alert("You can select maximum of " + limit + " checkbox.");
				this.checked = false;
			}
		}
	}
}