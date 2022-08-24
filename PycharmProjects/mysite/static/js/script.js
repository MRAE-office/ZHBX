/* JavaScript with the precious help of Jean Pierre Vincent @theystolemynick https://twitter.com/theystolemynick  */

function validateThisField (field) {
	if (field.required && field.value === '') {
		field.classList.add('required');
		formIsValid = false;
	}
	if (field.pattern
			&& !(new RegExp(field.pattern).exec(field.value) !== null) ) {
		field.classList.add('invalid');
		formIsValid = false;
	}

}

var form = document.getElementById('loginform');
var fields = form.querySelectorAll('input');
var formIsValid = true;

form.addEventListener('submit', function (e) {
	e.preventDefault();
	Array.prototype.forEach.call(fields, validateThisField);
  	// also have a global state on the form
	if (!formIsValid) {
    form.classList.remove('errors');
        setTimeout(function() {form.classList.add('errors');}, 0);
    }
});
/*
 form.addEventListener('focus', function (e) {
	e.target.classList.remove('required');
	e.target.classList.remove('invalid');
}, true); */

form.addEventListener('blur', function (e) {
  e.target.classList.remove('required');
	e.target.classList.remove('invalid');
	validateThisField(e.target);
}, true);