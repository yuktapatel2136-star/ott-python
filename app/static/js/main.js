(function ($) {
  ("use strict");

  // Preloader
  window.addEventListener("load", function () {
    document.querySelector("body").classList.add("loaded");
  });

  //search bar script
  const search_btn = document.querySelector(".header_search_btn");
  const search_box = document.querySelector(".header_search_box");
  // show header search box
  if (search_btn) {
    search_btn.addEventListener("click", (e) => {
      e.preventDefault();
      e.target.classList.toggle("close");
      search_box.classList.toggle("show_box");
    });
  }
  // Hide search box when click outside
  if (search_box) {
    document.addEventListener("click", function (e) {
      if (
        e.target != search_btn &&
        search_box.classList.contains("show_box") &&
        !document.querySelector(".header_search_form").contains(e.target)
      ) {
        search_btn.classList.toggle("close");
        // search_box.classList.toggle("show_box");
      }
    });
  }

  // sidebar menu
  var sidebarMenu = $("#sidebar-menu");
  var bodyOvrelay = $("#body-overlay");
  $(document).on("click", ".close_button", function (e) {
    e.preventDefault();
    sidebarMenu.removeClass("show_menu");
  });
  $(document).on("click", "#navigation-button", function (e) {
    e.preventDefault();
    sidebarMenu.addClass("show_menu");
  });

  $(document).on("click", "#navigation-button2", function (e) {
    e.preventDefault();
    sidebarMenu.addClass("show_menu");
  });

  // navbar-click mobile menu
  $(".menu-item-has-children a").on("click", function () {
    var element = $(this).parent("li");
    if (element.hasClass("show")) {
      element.removeClass("show");
      element.children("ul").slideUp(500);
    } else {
      element.siblings("li").removeClass("show");
      element.addClass("show");
      element.siblings("li").find("ul").slideUp(500);
      element.children("ul").slideDown(500);
    }
  });

  const progressCircle = document.querySelector(".linear-circle");
  // Hero Slider
  new Swiper(".hero-slider-one", {
    speed: 1500,
    slidesPerView: "auto",
    centeredSlides: true,
    slideToClickedSlide: true,
    clickable: true,
    allowTouchMove: false,
    loop: true,
    autoplay: {
      delay: 10000,
      disableOnInteraction: false,
    },
    navigation: {
      prevEl: ".prev-slide",
      nextEl: ".next-slide",
    },
    on: {
      autoplayTimeLeft(s, time, progress) {
        progressCircle.style.setProperty("--progress", 1 - progress);
      },
    },
    breakpoints: {
      1366: {
        spaceBetween: -50,
      },
      1600: {
        spaceBetween: -70,
      },
    },
  });

  // Hero Card Slider
  new Swiper(".hero-card-slider-wrap", {
    speed: 500,
    effect: "cards",
    rotate: false,
    perSlideRotate: 2000,
    perSlideOffset: 500,
    pagination: {
      el: ".swiper-pagination",
      type: "fraction",
    },
  });

  new Swiper(".hero-slider-two", {
    speed: 1000,
    loop: true,
    autoplay: false,
    pagination: {
      el: ".swiper-pagination",
      type: "fraction",
    },
  });

  //movie-card-slider-sm
  new Swiper(".movie-card-slider-sm", {
    speed: 1000,
    spaceBetween: 10,
    loop: true,
    centeredSlides: true,
    breakpoints: {
      0: {
        slidesPerView: "1.2",
      },
      576: {
        slidesPerView: "1.7",
        spaceBetween: 20,
      },
      992: {
        slidesPerView: "2.5",
        spaceBetween: 20,
      },
      1366: {
        slidesPerView: "3.5",
        spaceBetween: 30,
      },
      1600: {
        slidesPerView: "3.9",
        spaceBetween: 30,
      },
    },
  });

  new Swiper(".movie-card-slider-sm-scroll", {
    speed: 9000,
    spaceBetween: 10,
    loop: true,
    centeredSlides: true,
    autoplay: {
      delay: 1,
      disableOnInteraction: true,
    },
    breakpoints: {
      0: {
        slidesPerView: "1.2",
      },
      576: {
        slidesPerView: "1.8",
      },
      992: {
        slidesPerView: "2.5",
        spaceBetween: 20,
      },
      1366: {
        slidesPerView: "3.5",
        spaceBetween: 30,
      },
      1600: {
        slidesPerView: "3.9",
        spaceBetween: 30,
      },
    },
  });

  new Swiper(".movie-card-slider-sm-reverse", {
    speed: 9000,
    slidesPerView: "auto",
    spaceBetween: 10,
    centeredSlides: true,
    loop: true,
    autoplay: {
      delay: 1,
      disableOnInteraction: true,
      reverseDirection: true,
    },
    breakpoints: {
      0: {
        slidesPerView: "1.2",
      },
      576: {
        slidesPerView: "1.8",
      },
      992: {
        slidesPerView: "2.5",
        spaceBetween: 20,
      },
      1366: {
        slidesPerView: "3.5",
        spaceBetween: 30,
      },
      1600: {
        slidesPerView: "3.9",
        spaceBetween: 30,
      },
    },
  });

  // Category Slider
  new Swiper(".categories-slider", {
    speed: 5000,
    spaceBetween: 10,
    loop: true,
    autoplay: true,
    autoplay: {
      delay: 1,
      pauseOnMouseEnter: true,
    },
    breakpoints: {
      0: { slidesPerView: "1" },
      576: { slidesPerView: "2" },
      768: { slidesPerView: "2" },
      992: { slidesPerView: "3" },
      1200: { slidesPerView: "4" },
      1500: { slidesPerView: "5" },
      1700: { slidesPerView: "6", spaceBetween: 30 },
    },
  });

  //Movie Slider Fluid
  new Swiper(".movie-slider-fluid", {
    speed: 1000,
    slidesPerView: "auto",
    spaceBetween: 30,
    centeredSlides: true,
    loop: true,
    slideToClickedSlide: true,
  });

  // Movie Slider Medium
  new Swiper(".rotate-movie-slider", {
    speed: 1000,
    slidesPerView: "auto",
    spaceBetween: 0,
    centeredSlides: true,
    loop: true,
    autoplay: {
      delay: 10000,
      disableOnInteraction: false,
    },
    slideToClickedSlide: true,
    effect: "coverflow",
    coverflowEffect: {
      rotate: 0,
      stretch: 10,
      depth: 0,
      modifier: 1,
      slideShadows: false,
    },
    navigation: {
      prevEl: ".prev-slide",
      nextEl: ".next-slide",
    },
    on: {
      autoplayTimeLeft(s, time, progress) {
        progressCircle.style.setProperty("--progress", 1 - progress);
      },
    },
  });

  new Swiper(".trending-slider-two", {
    slidesPerView: "auto",
    spaceBetween: 10,
    speed: 7000,
    loop: true,
    autoplay: {
      delay: 1,
      pauseOnMouseEnter: true,
    },
    breakpoints: {
      0: {
        slidesPerView: "1",
      },
      600: {
        slidesPerView: "2",
      },
      992: {
        slidesPerView: "3",
        spaceBetween: 20,
      },
      1366: {
        slidesPerView: "4",
        spaceBetween: 20,
      },
      1600: {
        slidesPerView: "4",
        spaceBetween: 30,
      },
    },
  });

  // Trending Movie Slider three
  new Swiper(".newest-release-slider", {
    speed: 500,
    spaceBetween: 20,
    centeredSlides: true,
    loop: true,
    navigation: {
      prevEl: ".newest-release-prev-slide",
      nextEl: ".newest-release-next-slide",
    },
    on: {
      autoplayTimeLeft(s, time, progress) {
        progressCircle.style.setProperty("--progress", 1 - progress);
      },
    },
    breakpoints: {
      0: {
        slidesPerView: "1.4",
      },
      576: {
        slidesPerView: "2",
      },
      768: {
        slidesPerView: "2",
      },
      992: {
        slidesPerView: "3.3",
        spaceBetween: 20,
        allowTouchMove: false,
      },
      1366: {
        slidesPerView: "5.3",
        spaceBetween: 20,
        allowTouchMove: false,
      },
    },
  });

  // Trending Movie Slider three
  new Swiper(".newest-release-slider2", {
    speed: 500,
    spaceBetween: 20,
    centeredSlides: true,
    loop: true,
    navigation: {
      prevEl: ".prev-slide2",
      nextEl: ".next-slide2",
    },
    breakpoints: {
      0: {
        slidesPerView: "1.4",
      },
      576: {
        slidesPerView: "2",
      },
      768: {
        slidesPerView: "2",
      },
      992: {
        slidesPerView: "3.3",
        spaceBetween: 20,
        allowTouchMove: false,
      },
      1366: {
        slidesPerView: "5.3",
        spaceBetween: 20,
        allowTouchMove: false,
      },
    },
  });

  // Trending Movie Slider three
  new Swiper(".newest-release-slider3", {
    speed: 8000,
    spaceBetween: 20,
    centeredSlides: true,
    loop: true,
    autoplay: {
      delay: 1,
      pauseOnMouseEnter: true,
    },
    breakpoints: {
      0: {
        slidesPerView: "1",
      },
      576: {
        slidesPerView: "2",
      },
      768: {
        slidesPerView: "2",
      },
      992: {
        slidesPerView: "3.3",
        spaceBetween: 20,
        allowTouchMove: false,
      },
      1366: {
        slidesPerView: "5.3",
        spaceBetween: 20,
        allowTouchMove: false,
      },
    },
  });

  // SHOWING VIDEO POPUP
  if ($(".popup_video").length) {
    $(".popup_video").magnificPopup({
      type: "iframe",
      mainClass: "video_fade",
      removalDelay: 160,
      preloader: false,
      fixedContentPos: false,
    });
  }

  /**---------------------------------------
   *  QTY Inputs
   * -------------------------------------*/
  $(function () {
    $("div.quantity").append(
      '<a class="inc qty-button">+</a><a class="dec qty-button">-</a>'
    );
    $(".qty-button").on("click", function () {
      console.log("clicked");
      var $button = $(this);
      var oldValue = $button.parent().find("input").val();

      if ($button.text() == "+") {
        var newVal = parseFloat(oldValue) + 1;
      } else {
        // Don't allow decrementing below zero
        if (oldValue > 0) {
          var newVal = parseFloat(oldValue) - 1;
        } else {
          newVal = 0;
        }
      }
      $button.parent().find("input").val(newVal);
    });
  });

  /*
    -----------------------------------------------------
    COURSE scroll up
    ----------------------------------------------------- 
    */
  const verticleSlider = new Swiper(".banner-3-varticle-slider", {
    direction: "vertical",
    slidesPerView: "auto",
    speed: 15000,
    loop: true,
    autoHeight: true,
    freeMode: false,
    autoplay: {
      delay: 0,
      reverseDirection: false,
      disableOnInteraction: false,
    },
  });

  /*
    -----------------------------------------------------
    COURSE scroll down
    ----------------------------------------------------- 
    */
  const verticleSliderDown = new Swiper(".banner-3-varticle-slider-two", {
    direction: "vertical",
    slidesPerView: "auto",
    speed: 15000,
    loop: true,
    autoHeight: true,
    freeMode: false,
    autoplay: {
      delay: 0,
      reverseDirection: true,
      disableOnInteraction: false,
    },
  });

  // Blog Slider
  new Swiper(".blog-slider-1", {
    speed: 1500,
    slidesPerView: 1,
    loop: true,
    autoplay: {
      delay: 10000,
      disableOnInteraction: false,
    },
    navigation: {
      prevEl: ".blog-prev-1",
      nextEl: ".blog-next-1",
    },
    spaceBetween: 30,
    breakpoints: {
      0: {
        slidesPerView: "1",
      },
      576: {
        slidesPerView: "1",
      },
      768: {
        slidesPerView: "2",
      },
    },
  });

  // Hero Slider 4
  new Swiper(".review-slider", {
    speed: 7000,
    loop: true,
    autoPlay: false,
    slidesPerView: "1",
    navigation: {
      prevEl: ".review-prev",
      nextEl: ".review-next",
    },
    autoplay: {
      delay: 1,
    },
  });

  var hero4Swiper = new Swiper(".hero-slider-4-thumbnail", {
    speed: 1500,
    spaceBetween: 10,
    slidesPerView: 2,
    loop: true,
    thumbs: {
      swiper: hero4Swiper2,
    },
  });

  //main-slider-4
  var hero4Swiper2 = new Swiper(".hero-slider-4", {
    speed: 1500,
    slidesPerView: "auto",
    loop: true,
    autoplay: {
      delay: 10000,
      disableOnInteraction: false,
    },
    spaceBetween: 20,
    effect: "fade",
    navigation: {
      nextEl: ".hero-4-next-slide",
      prevEl: ".hero-4-prev-slide",
    },
    on: {
      autoplayTimeLeft(s, time, progress) {
        progressCircle.style.setProperty("--progress", 1 - progress);
      },
    },
    pagination: {
      el: ".hero-4-pagination",
      type: "fraction",
    },
    thumbs: {
      swiper: hero4Swiper,
    },
  });

  //home 4 scroll slider
  const scrollSliderLeft = new Swiper(".home-4-scroll-slider", {
    spaceBetween: 20,
    speed: 9000,
    loop: true,
    autoplay: {
      delay: 1,
      disableOnInteraction: false,
    },
    breakpoints: {
      2000: {
        slidesPerView: 3.1,
      },
      1599: {
        slidesPerView: 2.6,
      },
      1200: {
        slidesPerView: 1.7,
      },
      991: {
        slidesPerView: 1.7,
      },
      700: {
        slidesPerView: 1.5,
      },
      576: {
        slidesPerView: 1.1,
      },
      376: {
        slidesPerView: 1,
      },
      0: {
        slidesPerView: 1,
        centeredSlides: true,
      },
    },
  });

  //home 4 3d slider
  new Swiper(".swiper-3d-slider .swiper-container", {
    effect: "coverflow",
    centeredSlides: true,
    speed: 500,
    loop: true,
    slidesPerView: 5.5,
    allowTouchMove: false,
    coverflowEffect: {
      rotate: -2,
      modifier: -1,
      slideShadows: false,
    },
    autoplay: {
      delay: 1000,
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: ".hero-4-3d-next-slide",
      prevEl: ".hero-4-3d-prev-slide",
    },
    pagination: {
      el: ".hero-4-3d-slider-pagination",
      type: "fraction",
    },
    breakpoints: {
      0: {
        slidesPerView: "1",
        coverflowEffect: {
          stretch: "-98%",
        },
      },
      600: {
        slidesPerView: "2",
        coverflowEffect: {
          stretch: "-98%",
        },
      },
      992: {
        slidesPerView: "5.5",
        coverflowEffect: {
          stretch: "-95%",
        },
      },
      1024: {
        slidesPerView: "3.5",
        coverflowEffect: {
          stretch: "-95%",
        },
      },
      1366: {
        slidesPerView: "5.5",
        coverflowEffect: {
          stretch: "-80%",
        },
      },
    },
  });

  //home 4 3d slider
  new Swiper(".swiper-3d-slider-2 .swiper-container", {
    effect: "coverflow",
    centeredSlides: true,
    speed: 500,
    loop: true,
    slidesPerView: 5.5,
    allowTouchMove: false,
    coverflowEffect: {
      rotate: -2,
      modifier: -1,
      slideShadows: false,
    },
    autoplay: {
      delay: 3000,
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: ".hero-4-3d-next-slide",
      prevEl: ".hero-4-3d-prev-slide",
    },
    pagination: {
      el: ".hero-4-3d-slider-pagination",
      type: "fraction",
    },
    breakpoints: {
      0: {
        slidesPerView: "1",
        coverflowEffect: {
          stretch: "-98%",
        },
      },
      600: {
        slidesPerView: "2",
        coverflowEffect: {
          stretch: "-98%",
        },
      },
      992: {
        slidesPerView: "5.5",
        coverflowEffect: {
          stretch: "-95%",
        },
      },
      1024: {
        slidesPerView: "3.5",
        coverflowEffect: {
          stretch: "-95%",
        },
      },
      1366: {
        slidesPerView: "5.5",
        coverflowEffect: {
          stretch: "-65%",
        },
      },
    },
  });

  new Swiper(".category-slider", {
    spaceBetween: 20,
    speed: 9000,
    loop: true,
    autoplay: {
      delay: 1,
      disableOnInteraction: false,
    },
    breakpoints: {
      0: {
        slidesPerView: "1",
      },
      600: {
        slidesPerView: "2",
      },
      992: {
        slidesPerView: "3",
      },
      1024: {
        slidesPerView: "3.5",
      },
      1366: {
        slidesPerView: "5.5",
      },
      1600: {
        slidesPerView: "4.5",
      },
    },
  });

  //artist-slider-active
  new Swiper(".artist-slider-active", {
    speed: 1500,
    spaceBetween: 10,
    loop: true,
    centeredSlides: true,
    breakpoints: {
      0: {
        slidesPerView: "1.2",
      },
      576: {
        slidesPerView: "1.7",
        spaceBetween: 20,
      },
      992: {
        slidesPerView: "2.5",
        spaceBetween: 20,
      },
      1366: {
        slidesPerView: "3.5",
        spaceBetween: 30,
      },
      1600: {
        slidesPerView: "3.8",
        spaceBetween: 30,
      },
      2000: {
        slidesPerView: "4.8",
        spaceBetween: 30,
      },
    },
  });

  // Playlist slider
  const progressCircle_2 = document.querySelector(".linear-circle");
  new Swiper(".playlist-slider-active", {
    speed: 1500,
    effect: "coverflow",
    slideToClickedSlide: true,
    clickable: true,
    allowTouchMove: false,
    spaceBetween: 0,
    slidesPerView: 3.5,
    loop: true,
    coverflowEffect: {
      rotate: -4,
      stretch: "-40%",
      modifier: -1,
      slideShadows: false,
    },
    navigation: {
      prevEl: ".prev-slide",
      nextEl: ".next-slide",
    },
    on: {
      autoplayTimeLeft(s, time, progress) {
        progressCircle_2.style.setProperty("--progress", 1 - progress);
      },
    },
    breakpoints: {
      0: {
        slidesPerView: "1.2",
      },
      576: {
        slidesPerView: "1.7",
      },
      992: {
        slidesPerView: "4",
      },
      1366: {
        slidesPerView: "5",
      },
      1600: {
        slidesPerView: "3.5",
      },
    },
  });

  // Hero slider five
  new Swiper(".hero-slide-active-5", {
    speed: 1500,
    slideToClickedSlide: true,
    clickable: true,
    spaceBetween: 0,
    slidesPerView: 3,
    loop: true,
    autoPlay: true,
    centeredSlides: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false,
    },
    breakpoints: {
      0: {
        slidesPerView: "1.2",
      },
      576: {
        slidesPerView: "1.5",
      },
      992: {
        slidesPerView: "2.5",
      },
      1366: {
        slidesPerView: "3",
      },
      1600: {
        slidesPerView: "2.5",
      },
    },
  });
})(jQuery, window);
