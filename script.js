document.addEventListener('DOMContentLoaded', () => {
    // Add smooth reveal animation to sections
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Initial state for sections
    document.querySelectorAll('section').forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        section.style.transition = 'all 0.6s ease-out';
        observer.observe(section);
    });

    // Handle contact link clicks
    document.querySelectorAll('.contact-item a').forEach(link => {
        link.addEventListener('click', (e) => {
            // Log interaction or handle analytics if needed
            console.log(`Contact link clicked: ${link.getAttribute('href')}`);
        });
    });

    // Avatar upload functionality
    const avatarInput = document.getElementById('avatar-input');
    const profileAvatar = document.getElementById('profile-avatar');
    
    if (avatarInput && profileAvatar) {
        avatarInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (!file) return;
            
            // Check file type
            if (!file.type.match('image.*')) {
                alert('请选择图片文件 (JPG, PNG, GIF 等)');
                return;
            }
            
            // Check file size (max 2MB)
            if (file.size > 2 * 1024 * 1024) {
                alert('图片大小不能超过 2MB');
                return;
            }
            
            const reader = new FileReader();
            
            reader.onload = function(e) {
                // Update avatar image
                profileAvatar.src = e.target.result;
                
                // Save to localStorage for persistence
                try {
                    localStorage.setItem('resume_avatar', e.target.result);
                    console.log('头像已保存到本地存储');
                } catch (error) {
                    console.warn('无法保存头像到本地存储:', error);
                }
            };
            
            reader.onerror = function() {
                alert('读取图片失败，请重试');
            };
            
            reader.readAsDataURL(file);
        });
        
        // Load saved avatar from localStorage on page load
        try {
            const savedAvatar = localStorage.getItem('resume_avatar');
            if (savedAvatar) {
                profileAvatar.src = savedAvatar;
            }
        } catch (error) {
            console.warn('无法从本地存储加载头像:', error);
        }
    }
    
    // Avatar reset functionality (optional)
    const resetAvatar = () => {
        const defaultAvatar = 'avatar.jpeg';
        profileAvatar.src = defaultAvatar;
        localStorage.removeItem('resume_avatar');
        if (avatarInput) avatarInput.value = '';
    };
    
    // Add reset button (optional, uncomment if needed)
    // const resetBtn = document.createElement('button');
    // resetBtn.textContent = '恢复默认头像';
    // resetBtn.className = 'avatar-upload-btn';
    // resetBtn.style.marginTop = '5px';
    // resetBtn.onclick = resetAvatar;
    // document.querySelector('.avatar-upload').appendChild(resetBtn);

    // PDF Export/Print functionality
    const printPdfBtn = document.getElementById('print-pdf-btn');
    if (printPdfBtn) {
        printPdfBtn.addEventListener('click', () => {
            // Hide navigation links during print
            const navLinks = document.querySelector('.nav-links');
            const originalDisplay = navLinks.style.display;
            navLinks.style.display = 'none';
            
            // Print the page
            window.print();
            
            // Restore navigation links after print
            setTimeout(() => {
                navLinks.style.display = originalDisplay || 'flex';
            }, 100);
        });
    }
});
