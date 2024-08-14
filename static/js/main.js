document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.toggle-comments').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            const commentsSection = document.getElementById(`comments-${postId}`);

            // Toggle class to show/hide comments
            commentsSection.classList.toggle('hidden');

            // Update button text based on visibility
            if (commentsSection.classList.contains('hidden')) {
                this.textContent = 'Show Comments';
            } else {
                this.textContent = 'Hide Comments';
            }
        });
    });
});