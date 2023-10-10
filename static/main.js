//
//
//
//// static/main.js
//
//console.log("Sanity check!");
//
//// Get Stripe publishable key
//fetch("/config/")
//.then((result) => { return result.json(); })
//.then((data) => {
//  // Initialize Stripe.js
//  const stripe = Stripe(data.publicKey);
//
//  // new
//  // Event handler
//  document.querySelector("#submitBtn").addEventListener("click", () => {
//    // Get Checkout Session ID
//    fetch("/create-checkout-session/")
//    .then((result) => { return result.json(); })
//    .then((data) => {
//      console.log(data);
//      // Redirect to Stripe Checkout
//      return stripe.redirectToCheckout({sessionId: data.sessionId})
//    })
//    .then((res) => {
//      console.log(res);
//    });
//  });
//});
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//


//console.log("Sanity check!");
//
//// Get Stripe publishable key
//fetch("/config/")
//  .then((result) => {
//    return result.json();
//  })
//  .then((data) => {
//    // Initialize Stripe.js
//    const stripe = Stripe(data.publicKey);
//
//    function getCookie(name) {
//      let cookieValue = null;
//      if (document.cookie && document.cookie !== '') {
//        const cookies = document.cookie.split(';');
//        for (let i = 0; i < cookies.length; i++) {
//          const cookie = cookies[i].trim();
//          // Does this cookie string begin with the name we want?
//          if (cookie.substring(0, name.length + 1) === (name + '=')) {
//            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//            break;
//          }
//        }
//      }
//      return cookieValue;
//    }
//
//    document.querySelector("#submitBtn").addEventListener("click", () => {
//      const paymentId = $('#submitBtn').attr("data-payment-id");
//      console.log(paymentId)
//      // Get Checkout Session ID
//      fetch("/create-checkout-session/", {
//        method: 'POST',
//        headers: {
//          'Content-Type': 'application/json',
//          'X-CSRFToken': getCookie('csrftoken')
//        },
//        body: JSON.stringify({ payment_id: paymentId })
//      })
//      .then((result) => {
//        return result.json();
//      })
//      .then((data) => {
//
//        console.log(data); // Confirm that data from the server is correctly logged
//
//        // Redirect to Stripe Checkout with line items
//        return stripe.redirectToCheckout({
//            sessionId: data.sessionId, // Use the session ID received from the server
//            lineItems: [
//                // Define the line items here
//                {
//                    price: 'price_1NvDCuSAMEcakUFvTHOBENjW', // Replace with the actual price ID from your Stripe Dashboard
//                    quantity: 1 // Specify the quantity
//                }
//                // Add more line items if needed
//            ]
//        });
//    })
//      .then((res) => {
//        console.log(res);
//      })
//      .catch((error) => {
//        console.error(error);
//      });
//    });
//  });

//   Event handler
//  document.querySelector("#submitBtn").addEventListener("click", () => {
//     const paymentId = $('#submitBtn').attr("data-payment-id");
//    fetch("/create-checkout-session/")
//    .then((result) => { return result.json(); })
//    .then((data) => {
//      console.log(data);
//      // Redirect to Stripe Checkout
//      return stripe.redirectToCheckout({sessionId: data.sessionId})
//    })
//    .then((res) => {
//      console.log(res);

// static/main.js

//console.log("Sanity check!");
//
//// Get Stripe publishable key
//fetch("/config/")
//.then((result) => { return result.json(); })
//.then((data) => {
//  // Initialize Stripe.js
//  const stripe = Stripe(data.publicKey);
//
//  // new
//  // Event handler
//  document.querySelector("#submitBtn").addEventListener("click", () => {
//    // Get Checkout Session ID
//    fetch("/create-checkout-session/")
//    .then((result) => { return result.json(); })
//    .then((data) => {
//      console.log(data);
//      // Redirect to Stripe Checkout
//      return stripe.redirectToCheckout({sessionId: data.sessionId})
//    })
//    .then((res) => {
//      console.log(res);
//    });
//  });
//});