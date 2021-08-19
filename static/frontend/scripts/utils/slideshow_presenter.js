let myIndex = 0;

function slideShow() {
    let i;
    const slideContainer = document.getElementsByClassName("mySlides");
    for (i = 0; i < slideContainer.length; i++) {
        slideContainer[i].style.display = "none";
    }
    myIndex++;
    if (myIndex > slideContainer.length) { myIndex = 1 }
    slideContainer[myIndex - 1].style.display = "block";
    setTimeout(slideShow, 5000); // Change image every 2 seconds
};

slideShow();