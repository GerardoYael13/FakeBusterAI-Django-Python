/**
 * Loading state handler for form submission
 */
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                const textSpan = submitBtn.querySelector('.btn-text');
                const loaderSpan = submitBtn.querySelector('.btn-loader');
                const loadingTextSpan = submitBtn.querySelector('.btn-loading-text');

                if (textSpan && loaderSpan && loadingTextSpan) {
                    textSpan.hidden = true;
                    textSpan.style.display = 'none';
                    loaderSpan.style.display = 'inline-block';
                    loadingTextSpan.hidden = false;
                    loadingTextSpan.style.display = 'inline-block';
                }
            }
        });
    });
});
