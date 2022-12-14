function refresh() {
    mplot = 'mplot.svg#'+Date.now()
    fetch(mplot,  { cache: 'reload', mode: 'same-origin' })
        .then((r) => {
	    console.log(r)
	    new_img = document.createElement('img')
	    new_img.src = mplot
	    old_img = document.getElementById('mplotdiv').children[1]
	    old_img.replaceWith(new_img)
	    console.log(mplot)
        })
    hplot = 'hplot.svg#'+Date.now()
    fetch(hplot,  { cache: 'reload', mode: 'same-origin' })
        .then((r) => {
	    console.log(r)
	    new_img = document.createElement('img')
	    new_img.src = hplot
	    old_img = document.getElementById('hplotdiv').children[1]
	    old_img.replaceWith(new_img)
	    console.log(hplot)
        })
    dplot = 'dplot.svg#'+Date.now()
    fetch(dplot,  { cache: 'reload', mode: 'same-origin' })
        .then((r) => {
	    console.log(r)
	    new_img = document.createElement('img')
	    new_img.src = dplot
	    old_img = document.getElementById('dplotdiv').children[1]
	    old_img.replaceWith(new_img)
	    console.log(hplot)
        })
}
window.addEventListener('load', (event) => {
    window.setInterval('refresh()', 8000); // 8 or80 seconds
});    
