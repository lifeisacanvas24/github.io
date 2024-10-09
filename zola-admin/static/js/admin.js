// /static/js/script.js

async function fetchOrders() {
    const response = await fetch('/admin/orders', {
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token') // Store token in local storage
        }
    });

    if (response.ok) {
        const orders = await response.json();
        const ordersList = document.getElementById('orders');
        ordersList.innerHTML = ''; // Clear existing orders

        orders.forEach(order => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${order.id}</td>
                <td>${order.user_id}</td>
                <td>${order.product_id}</td>
                <td>${order.service_id}</td>
                <td>${order.status}</td>
            `;
            ordersList.appendChild(row);
        });
    } else {
        console.error('Failed to fetch orders:', response.statusText);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchOrders();

    // Initialize SimpleMDE
    const simplemde = new SimpleMDE({ element: document.getElementById("markdownEditor") });

    // Handle post submission
    document.getElementById('submitPost').addEventListener('click', async () => {
        const content = simplemde.value();
        const title = prompt("Enter the title for the post:");
        const category = prompt("Enter the category for the post:");

        if (!title || !category) {
            alert("Title and category are required!");
            return;
        }

        const postData = {
            title: title,
            content: content,
            category: category
        };

        const response = await fetch('/api/posts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token') // Use stored token
            },
            body: JSON.stringify(postData)
        });

        if (response.ok) {
            alert("Post submitted successfully!");
            simplemde.value(''); // Clear the editor
            fetchOrders(); // Refresh the orders
        } else {
            alert("Failed to submit post: " + response.statusText);
        }
    });
});
