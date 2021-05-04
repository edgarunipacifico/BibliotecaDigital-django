//selecionamos todas las img que estan dentro de un  ccontenedor modal
document.querySelectorAll(".modal-container img").forEach(funcion=>{
    //cuando damos clicka la imagen
    
    funcion.addEventListener("click",function (ev) {
       ev.stopPropagation();
        this.parentNode.ClassList.add(active);
    })
})

document.querySelectorAll(".modal-container").forEach(funcion=>{
    //cerrar el modal cuando damos clic por fuera de la imagen
    funcion.addEventListener("click",function (ev) {
        this.parentNode.ClassList.remove(active);
    })
})
