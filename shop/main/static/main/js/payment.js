const stripe = Stripe(publishableKey);

let currentElements = null;
let currentClientSecret = null;

function showPaymentForm() {
    document.getElementById('payment-form').classList.remove('hidden');
}

function hidePaymentForm() {
    document.getElementById('payment-form').classList.add('hidden');
}

function initStripePayment(clientSecret) {
    currentClientSecret = clientSecret;
    currentElements = stripe.elements({ clientSecret: clientSecret });
    const paymentElement = currentElements.create('payment');
    paymentElement.mount('#card-element');
}

document.getElementById('submit-payment').onclick = async () => {
    if (!currentElements || !currentClientSecret) return;

    await currentElements.submit();

    await stripe.confirmPayment({
        elements: currentElements,
        clientSecret: currentClientSecret,
        confirmParams: {
            return_url: window.location.origin + '/success/'
        }
    });
};

document.getElementById('cancel-payment').onclick = () => {
    hidePaymentForm();
};

const buyFromItemButton = document.getElementById('buy-from-item-button');
if (buyFromItemButton) {
    buyFromItemButton.onclick = () => {
        const itemId = buyFromItemButton.dataset.itemId;

        fetch('/buy/${itemId}')
            .then(response => response.json())
            .then(data => {
                initStripePayment(data.clientSecret);
                showPaymentForm();
            });
    };
}

const buyFromCartButton = document.getElementById('buy-from-cart-button');
if (buyFromCartButton) {
    buyFromCartButton.onclick = () => {
        fetch('/buy/')
            .then(response => response.json())
            .then(data => {
                initStripePayment(data.clientSecret);
                showPaymentForm();
            });
    };
}

