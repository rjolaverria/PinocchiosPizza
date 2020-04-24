document.addEventListener('DOMContentLoaded', () => {
  // Global variables
  const item = document.getElementById('item');
  const extras = document.getElementsByClassName('topping');
  const sizes = document.getElementsByName('size');
  let allowedChecked = 0;
  let checkCount = 0;

  // Check state helper
  const updateCheckState = () => {
    for (extra of extras) {
      if (checkCount === allowedChecked && extra.checked == false) {
        extra.disabled = true;
      } else {
        extra.disabled = false;
      }
    }
  };
  updateCheckState();

  // Update Allowed Amount
  item.addEventListener('change', () => {
    switch (Number(item.value)) {
      case 0:
      case 1:
      case 6:
        allowedChecked = 0;
        break;
      case 2:
      case 7:
        allowedChecked = 1;
        break;
      case 3:
      case 8:
        allowedChecked = 2;
        break;
      case 4:
      case 9:
        allowedChecked = 3;
        break;
      default:
        allowedChecked = 20;
        break;
    }
    updateCheckState();
  });

  // Update check state
  for (extra of extras) {
    extra.addEventListener('click', (e) => {
      let checked = 0;
      for (extra of extras) {
        if (extra.checked) {
          checked++;
        }
      }
      checkCount = checked;
      updateCheckState();
    });
  }

  // Add Item to cart
  document.querySelector('#item-form').onsubmit = (e) => {
    e.preventDefault();

    // Data to send
    const token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    const itemId = item.value;
    let selectedSize;
    const selectedExtras = [];
    for (let i = 0; i < extras.length; i++) {
      if (extras.item(i).checked) {
        selectedExtras.push(extras.item(i).value);
      }
    }
    for (let i = 0; i < sizes.length; i++) {
      if (sizes[i].checked) {
        selectedSize = sizes[i].value;
      }
    }

    // Send Data
    const url = `${location.protocol}//${document.domain}:${location.port}/add_item`;
    fetch(url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': token,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: JSON.stringify({
        itemId,
        extras: selectedExtras,
        size: selectedSize,
      }),
    }).then((res) => {
      // Update cart count
      res
        .json()
        .then((e) => (document.querySelector('.cart-count').innerHTML = e));

      // Display Alert
      let alert = document.querySelector('.alert');
      alert.classList.remove('d-none');
      setTimeout(() => alert.classList.add('d-none'), 5000);

      // Reset Form Data
      document.querySelector('#item-form').reset();
      allowedChecked = 20;
      updateCheckState();
    });
  };
});
