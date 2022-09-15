function refresh() {
    line = 'line.svg#'+Date.now()
    fetch(line,  { cache: 'reload', mode: 'same-origin' })
        .then((r) => {
	    console.log(r)
	    new_img = document.createElement('img')
	    new_img.height = "600"
	    new_img.src = line
	    old_img = document.getElementById('imgdiv').children[0]
	    old_img.replaceWith(new_img)
	    console.log(line)
        })
}
window.addEventListener('load', (event) => {
    window.setInterval('refresh()', 8000); // 8 or80 seconds
});    
