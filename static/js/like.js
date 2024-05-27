document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('#likeButton').forEach(button => {
        button.addEventListener('click', function() {
            const propertyId = this.getAttribute('data-property-id');
            fetch(`/property/${propertyId}/like/`, { method: 'POST', credentials: 'same-origin' })
                .then(response => response.json())
                .then(data => {
                    const likeCount = document.querySelector(`#likeCount-${propertyId}`);
                    likeCount.textContent = data.likes_count;
                    const likeIcon = document.querySelector(`#likeIcon-${propertyId}`);
                    likeIcon.textContent = data.is_liked ? 'favorite' : 'favorite_border';
                })
                .catch(error => console.error('Error:', error));
        });
    });
});
