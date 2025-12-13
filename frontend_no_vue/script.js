// 用户系统相关变量
let currentUser = null;
let userData = JSON.parse(localStorage.getItem('web_auto_users')) || {};
let isRegisterMode = false;

// 等待页面加载完成
document.addEventListener('DOMContentLoaded', function() {
    // 初始化用户状态
    initializeUserState();
    
    // 获取所有带下拉菜单的导航项
    const dropdownItems = document.querySelectorAll('.nav-item.dropdown');
    
    // 遍历 dropdownItems 中的每一个元素，item 是当前遍历的元素
    dropdownItems.forEach(function(item) {
        // 在当前下拉菜单项内查找下拉切换按钮
        const toggleBtn = item.querySelector('.dropdown-toggle');
        
        // 为下拉切换按钮添加点击事件监听器，e 是事件对象
        toggleBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // 切换当前下拉菜单项（item）的'active'类
            item.classList.toggle('active');
        });
    });
    
    // 阻止下拉菜单内部点击事件冒泡
    const dropdownMenus = document.querySelectorAll('.dropdown-menu');
    dropdownMenus.forEach(function(menu) {
        menu.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    });
    
    // 为所有导航链接添加点击事件（除下拉切换按钮外）
    const navLinks = document.querySelectorAll('.nav-link:not(.dropdown-toggle)');
    navLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            // 为当前点击的父项添加active类
            this.closest('.nav-item').classList.add('active');
        });
    });

    // ============================================
    // 用户系统功能
    // ============================================
    
    // 登录按钮事件
    document.getElementById('loginBtn').addEventListener('click', function() {
        openAuthModal(false);
    });
    
    // 退出按钮事件
    document.getElementById('logoutBtn').addEventListener('click', function() {
        logout();
    });
    
    // 初始化认证模态窗口事件
    setupAuthModalEvents();
    
    // ============================================
    // 服务器信息相关功能
    // ============================================
    
    // 初始化密码掩码
    initializePasswordMasks();
    
    // 绑定显示/隐藏密码按钮事件
    document.querySelectorAll('.show-password-btn').forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const passwordElement = document.getElementById(targetId);
            
            if (passwordElement.classList.contains('password-visible')) {
                // 切换到隐藏状态
                passwordElement.classList.remove('password-visible');
                this.innerHTML = '<i class="fas fa-eye"></i>';
            } else {
                // 切换到显示状态
                passwordElement.classList.add('password-visible');
                this.innerHTML = '<i class="fas fa-eye-slash"></i>';
            }
        });
    });
    
    // 绑定复制按钮事件
    document.querySelectorAll('.copy-btn').forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const targetElement = document.getElementById(targetId);
            let textToCopy;
            
            // 如果是密码，从data-password属性获取
            if (targetElement.hasAttribute('data-password')) {
                textToCopy = targetElement.getAttribute('data-password');
            } else {
                // 其他信息直接获取文本内容
                textToCopy = targetElement.textContent;
            }
            
            // 复制到剪贴板
            navigator.clipboard.writeText(textToCopy).then(() => {
                const originalIcon = this.innerHTML;
                this.innerHTML = '<i class="fas fa-check"></i>';
                
                setTimeout(() => {
                    this.innerHTML = originalIcon;
                }, 1500);
            }).catch(err => {
                console.error('复制失败:', err);
                alert('复制失败，请手动复制');
            });
        });
    });

    // ============================================
    // 修改信息模态窗口相关
    // ============================================
    
    // 绑定修改信息按钮事件（BMC和OS都要绑定）
    document.getElementById('edit-bmc').addEventListener('click', function() {
        openEditModal('bmc');
    });
    
    document.getElementById('edit-os').addEventListener('click', function() {
        openEditModal('os');
    });
    
    // 绑定测试连接按钮事件
    document.getElementById('test-bmc-connection').addEventListener('click', function() {
        testConnection('BMC');
    });
    
    document.getElementById('test-os-connection').addEventListener('click', function() {
        testConnection('OS');
    });

    // 初始化模态窗口事件
    setupModalEvents();
    
    // 初始化密码验证
    setupPasswordValidation();
    
    // 按ESC键关闭模态窗口
    document.addEventListener('keydown', function(event) {
        const editModal = document.getElementById('editModal');
        const authModal = document.getElementById('authModal');
        
        if (event.key === 'Escape') {
            if (editModal.classList.contains('active')) {
                closeEditModal();
            }
            if (authModal.classList.contains('active')) {
                closeAuthModal();
            }
        }
    });
});

// ============================================
// 通用函数定义
// ============================================

// 用户系统函数
function initializeUserState() {
    // 从localStorage获取当前用户
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
        currentUser = savedUser;
        updateUIForLoggedInUser();
        loadUserData();
    }
}

function updateUIForLoggedInUser() {
    const welcomeText = document.getElementById('welcomeText');
    const loginBtn = document.getElementById('loginBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    
    if (currentUser) {
        welcomeText.textContent = `欢迎，${currentUser}`;
        loginBtn.style.display = 'none';
        logoutBtn.style.display = 'block';
        
        // 启用所有功能
        document.querySelectorAll('.info-actions .btn').forEach(btn => {
            btn.disabled = false;
        });
    } else {
        welcomeText.textContent = '欢迎，请登录';
        loginBtn.style.display = 'block';
        logoutBtn.style.display = 'none';
        
        // 禁用所有功能
        document.querySelectorAll('.info-actions .btn').forEach(btn => {
            btn.disabled = true;
        });
    }
}

function openAuthModal(isRegister) {
    const authModal = document.getElementById('authModal');
    const authTitle = document.getElementById('authTitle');
    const switchText = document.getElementById('switchText');
    const switchBtn = document.getElementById('switchBtn');
    const submitBtn = document.getElementById('submitAuth');
    const authForm = document.getElementById('authForm');
    
    isRegisterMode = isRegister;
    
    if (isRegister) {
        authTitle.textContent = '用户注册';
        switchText.textContent = '已有账户？';
        switchBtn.textContent = '立即登录';
        submitBtn.textContent = '注册';
    } else {
        authTitle.textContent = '用户登录';
        switchText.textContent = '还没有账户？';
        switchBtn.textContent = '立即注册';
        submitBtn.textContent = '登录';
    }
    
    // 重置表单
    authForm.reset();
    
    // 显示模态窗口
    authModal.classList.add('active');
    document.getElementById('auth-username').focus();
}

function closeAuthModal() {
    const authModal = document.getElementById('authModal');
    authModal.classList.remove('active');
}

function setupAuthModalEvents() {
    const authModal = document.getElementById('authModal');
    const modalCloseBtn = authModal.querySelector('.modal-close');
    const cancelAuthBtn = document.getElementById('cancelAuth');
    const authForm = document.getElementById('authForm');
    const switchBtn = document.getElementById('switchBtn');
    
    // 关闭模态窗口
    function closeModal() {
        authModal.classList.remove('active');
    }
    
    // 点击关闭按钮
    if (modalCloseBtn) {
        modalCloseBtn.addEventListener('click', closeModal);
    }
    
    // 点击取消按钮
    if (cancelAuthBtn) {
        cancelAuthBtn.addEventListener('click', closeModal);
    }
    
    // 点击模态窗口外部关闭
    if (authModal) {
        authModal.addEventListener('click', function(event) {
            if (event.target === authModal) {
                closeModal();
            }
        });
    }
    
    // 切换登录/注册模式
    if (switchBtn) {
        switchBtn.addEventListener('click', function() {
            openAuthModal(!isRegisterMode);
        });
    }
    
    // 表单提交事件
    if (authForm) {
        authForm.addEventListener('submit', function(event) {
            event.preventDefault();
            handleAuthSubmit();
        });
    }
    
    // 绑定密码显示/隐藏按钮
    authModal.querySelectorAll('.toggle-password-btn').forEach(button => {
        button.addEventListener('click', function() {
            const passwordInput = this.parentElement.querySelector('.password-input');
            const eyeIcon = this.querySelector('i');
            
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                eyeIcon.className = 'fas fa-eye-slash';
            } else {
                passwordInput.type = 'password';
                eyeIcon.className = 'fas fa-eye';
            }
        });
    });
}

function handleAuthSubmit() {
    const username = document.getElementById('auth-username').value.trim();
    const password = document.getElementById('auth-password').value;
    
    if (!username || !password) {
        alert('请填写用户名和密码');
        return;
    }
    
    if (isRegisterMode) {
        // 注册逻辑
        if (userData[username]) {
            alert('用户名已存在，请使用其他用户名');
        } else {
            // 保存用户数据
            userData[username] = {
                password: password,
                bmc: { ip: '', username: '', password: '' },
                os: { ip: '', username: '', password: '' }
            };
            
            // 保存到localStorage
            localStorage.setItem('web_auto_users', JSON.stringify(userData));
            
            alert('注册成功！请登录');
            
            // 切换到登录模式
            openAuthModal(false);
        }
    } else {
        // 登录逻辑
        if (userData[username] && userData[username].password === password) {
            currentUser = username;
            localStorage.setItem('currentUser', username);
            
            updateUIForLoggedInUser();
            loadUserData();
            closeAuthModal();
            
            alert(`欢迎回来，${username}！`);
        } else {
            alert('用户名或密码错误，请检查或注册新账户');
        }
    }
}

function logout() {
    currentUser = null;
    localStorage.removeItem('currentUser');
    
    updateUIForLoggedInUser();
    clearUserData();
    
    alert('已退出登录');
}

function loadUserData() {
    if (!currentUser || !userData[currentUser]) return;
    
    const user = userData[currentUser];
    
    // 加载BMC数据
    if (user.bmc.ip) {
        document.getElementById('bmc-ip').textContent = user.bmc.ip;
        document.getElementById('bmc-username').textContent = user.bmc.username;
        
        if (user.bmc.password) {
            const bmcPasswordElement = document.getElementById('bmc-password');
            bmcPasswordElement.setAttribute('data-password', user.bmc.password);
            
            // 添加密码显示按钮
            const passwordContainer = bmcPasswordElement.closest('.info-item');
            if (!passwordContainer.querySelector('.show-password-btn')) {
                const showBtn = document.createElement('button');
                showBtn.className = 'show-password-btn';
                showBtn.setAttribute('data-target', 'bmc-password');
                showBtn.innerHTML = '<i class="fas fa-eye"></i>';
                passwordContainer.querySelector('.copy-btn').after(showBtn);
                
                // 重新绑定事件
                showBtn.addEventListener('click', function() {
                    const targetId = this.getAttribute('data-target');
                    const passwordElement = document.getElementById(targetId);
                    
                    if (passwordElement.classList.contains('password-visible')) {
                        passwordElement.classList.remove('password-visible');
                        this.innerHTML = '<i class="fas fa-eye"></i>';
                    } else {
                        passwordElement.classList.add('password-visible');
                        this.innerHTML = '<i class="fas fa-eye-slash"></i>';
                    }
                });
            }
        }
    }
    
    // 加载OS数据
    if (user.os.ip) {
        document.getElementById('os-ip').textContent = user.os.ip;
        document.getElementById('os-username').textContent = user.os.username;
        
        if (user.os.password) {
            const osPasswordElement = document.getElementById('os-password');
            osPasswordElement.setAttribute('data-password', user.os.password);
            
            // 添加密码显示按钮
            const passwordContainer = osPasswordElement.closest('.info-item');
            if (!passwordContainer.querySelector('.show-password-btn')) {
                const showBtn = document.createElement('button');
                showBtn.className = 'show-password-btn';
                showBtn.setAttribute('data-target', 'os-password');
                showBtn.innerHTML = '<i class="fas fa-eye"></i>';
                passwordContainer.querySelector('.copy-btn').after(showBtn);
                
                // 重新绑定事件
                showBtn.addEventListener('click', function() {
                    const targetId = this.getAttribute('data-target');
                    const passwordElement = document.getElementById(targetId);
                    
                    if (passwordElement.classList.contains('password-visible')) {
                        passwordElement.classList.remove('password-visible');
                        this.innerHTML = '<i class="fas fa-eye"></i>';
                    } else {
                        passwordElement.classList.add('password-visible');
                        this.innerHTML = '<i class="fas fa-eye-slash"></i>';
                    }
                });
            }
        }
    }
    
    // 重新初始化密码掩码
    initializePasswordMasks();
}

function clearUserData() {
    // 重置BMC数据
    document.getElementById('bmc-ip').textContent = '未设置';
    document.getElementById('bmc-username').textContent = '未设置';
    const bmcPasswordElement = document.getElementById('bmc-password');
    bmcPasswordElement.setAttribute('data-password', '');
    bmcPasswordElement.innerHTML = '未设置';
    const bmcShowBtn = document.querySelector('.show-password-btn[data-target="bmc-password"]');
    if (bmcShowBtn) bmcShowBtn.remove();
    
    // 重置OS数据
    document.getElementById('os-ip').textContent = '未设置';
    document.getElementById('os-username').textContent = '未设置';
    const osPasswordElement = document.getElementById('os-password');
    osPasswordElement.setAttribute('data-password', '');
    osPasswordElement.innerHTML = '未设置';
    const osShowBtn = document.querySelector('.show-password-btn[data-target="os-password"]');
    if (osShowBtn) osShowBtn.remove();
    
    // 重置状态为未连接
    document.querySelectorAll('.status-badge').forEach(badge => {
        badge.textContent = '未连接';
        badge.className = 'status-badge disconnected';
    });
}

// 修改保存函数以保存用户数据
function saveChanges() {
    if (!currentUser) {
        alert('请先登录');
        return;
    }
    
    const type = document.getElementById('edit-type').value;
    const newIp = document.getElementById('edit-ip').value.trim();
    const newUsername = document.getElementById('edit-username').value.trim();
    const newPassword = document.getElementById('edit-password').value;
    
    // 简单验证
    if (!newIp || !newUsername || !newPassword) {
        alert('请填写所有必填字段');
        return;
    }
    
    // IP地址验证
    const ipPattern = /^(\d{1,3}\.){3}\d{1,3}$/;
    if (!ipPattern.test(newIp)) {
        alert('请输入有效的IP地址');
        return;
    }
    
    // 保存到用户数据
    if (type === 'bmc') {
        userData[currentUser].bmc = {
            ip: newIp,
            username: newUsername,
            password: newPassword
        };
        
        // 更新页面显示
        document.getElementById('bmc-ip').textContent = newIp;
        document.getElementById('bmc-username').textContent = newUsername;
        document.getElementById('bmc-password').setAttribute('data-password', newPassword);
        document.getElementById('bmc-password').innerHTML = `
            <span class="password-text">${newPassword}</span>
            <span class="password-mask"></span>
        `;
        
        // 添加密码显示按钮
        const passwordContainer = document.getElementById('bmc-password').closest('.info-item');
        if (!passwordContainer.querySelector('.show-password-btn')) {
            const showBtn = document.createElement('button');
            showBtn.className = 'show-password-btn';
            showBtn.setAttribute('data-target', 'bmc-password');
            showBtn.innerHTML = '<i class="fas fa-eye"></i>';
            passwordContainer.querySelector('.copy-btn').after(showBtn);
            
            // 重新绑定事件
            showBtn.addEventListener('click', function() {
                const targetId = this.getAttribute('data-target');
                const passwordElement = document.getElementById(targetId);
                
                if (passwordElement.classList.contains('password-visible')) {
                    passwordElement.classList.remove('password-visible');
                    this.innerHTML = '<i class="fas fa-eye"></i>';
                } else {
                    passwordElement.classList.add('password-visible');
                    this.innerHTML = '<i class="fas fa-eye-slash"></i>';
                }
            });
        }
    } else if (type === 'os') {
        userData[currentUser].os = {
            ip: newIp,
            username: newUsername,
            password: newPassword
        };
        
        // 更新页面显示
        document.getElementById('os-ip').textContent = newIp;
        document.getElementById('os-username').textContent = newUsername;
        document.getElementById('os-password').setAttribute('data-password', newPassword);
        document.getElementById('os-password').innerHTML = `
            <span class="password-text">${newPassword}</span>
            <span class="password-mask"></span>
        `;
        
        // 添加密码显示按钮
        const passwordContainer = document.getElementById('os-password').closest('.info-item');
        if (!passwordContainer.querySelector('.show-password-btn')) {
            const showBtn = document.createElement('button');
            showBtn.className = 'show-password-btn';
            showBtn.setAttribute('data-target', 'os-password');
            showBtn.innerHTML = '<i class="fas fa-eye"></i>';
            passwordContainer.querySelector('.copy-btn').after(showBtn);
            
            // 重新绑定事件
            showBtn.addEventListener('click', function() {
                const targetId = this.getAttribute('data-target');
                const passwordElement = document.getElementById(targetId);
                
                if (passwordElement.classList.contains('password-visible')) {
                    passwordElement.classList.remove('password-visible');
                    this.innerHTML = '<i class="fas fa-eye"></i>';
                } else {
                    passwordElement.classList.add('password-visible');
                    this.innerHTML = '<i class="fas fa-eye-slash"></i>';
                }
            });
        }
    }
    
    // 保存到localStorage
    localStorage.setItem('web_auto_users', JSON.stringify(userData));
    
    // 重新初始化密码掩码
    initializePasswordMasks();
    
    // 显示保存成功消息
    alert('信息已成功更新！');
    
    // 关闭模态窗口
    closeEditModal();
}

// 以下为原有函数，保持不变...

function initializePasswordMasks() {
    document.querySelectorAll('.info-value[data-password]').forEach(element => {
        const password = element.getAttribute('data-password');
        const maskElement = element.querySelector('.password-mask');
        
        if (maskElement && password) {
            // 根据密码长度生成相应数量的星号
            const stars = '*'.repeat(password.length);
            maskElement.textContent = stars;
        }
    });
}

function openEditModal(type) {
    if (!currentUser) {
        alert('请先登录');
        return;
    }
    
    const modal = document.getElementById('editModal');
    const form = document.getElementById('editForm');
    
    // 根据类型设置标题和数据
    let title = '';
    let ip, username, password;
    
    if (type === 'bmc') {
        title = '修改 BMC 连接信息';
        const bmcData = userData[currentUser]?.bmc || {};
        ip = bmcData.ip || '';
        username = bmcData.username || '';
        password = bmcData.password || '';
    } else if (type === 'os') {
        title = '修改 OS 连接信息';
        const osData = userData[currentUser]?.os || {};
        ip = osData.ip || '';
        username = osData.username || '';
        password = osData.password || '';
    }
    
    // 更新模态窗口标题
    document.querySelector('.modal-header h3').innerHTML = `<i class="fas fa-edit"></i> ${title}`;
    
    // 填充表单数据
    document.getElementById('edit-ip').value = ip;
    document.getElementById('edit-username').value = username;
    document.getElementById('edit-password').value = password;
    document.getElementById('edit-confirm-password').value = password;
    document.getElementById('edit-type').value = type;
    document.getElementById('edit-original-ip').value = ip;
    document.getElementById('edit-original-username').value = username;
    
    // 重置表单状态
    form.reset();
    clearValidationErrors();
    
    // 显示模态窗口
    modal.classList.add('active');
    document.getElementById('edit-ip').focus();
}

function closeEditModal() {
    const editModal = document.getElementById('editModal');
    editModal.classList.remove('active');
}

function clearValidationErrors() {
    document.querySelectorAll('.form-input').forEach(input => {
        input.classList.remove('error');
    });
    
    const messageElement = document.querySelector('.password-match-message');
    if (messageElement) {
        messageElement.textContent = '';
        messageElement.className = 'password-match-message';
    }
    
    const saveButton = document.getElementById('saveEdit');
    if (saveButton) {
        saveButton.disabled = false;
    }
}

function setupModalEvents() {
    const editModal = document.getElementById('editModal');
    const modalCloseBtn = document.querySelector('.modal-close');
    const cancelEditBtn = document.getElementById('cancelEdit');
    const editForm = document.getElementById('editForm');
    
    // 关闭模态窗口
    function closeModal() {
        editModal.classList.remove('active');
    }
    
    // 点击关闭按钮
    if (modalCloseBtn) {
        modalCloseBtn.addEventListener('click', closeModal);
    }
    
    // 点击取消按钮
    if (cancelEditBtn) {
        cancelEditBtn.addEventListener('click', closeModal);
    }
    
    // 点击模态窗口外部关闭
    if (editModal) {
        editModal.addEventListener('click', function(event) {
            if (event.target === editModal) {
                closeModal();
            }
        });
    }
    
    // 表单提交事件
    if (editForm) {
        editForm.addEventListener('submit', function(event) {
            event.preventDefault();
            saveChanges();
        });
    }
    
    // 绑定模态窗口密码显示/隐藏按钮
    document.querySelectorAll('.toggle-password-btn').forEach(button => {
        button.addEventListener('click', function() {
            const passwordInput = this.parentElement.querySelector('.password-input');
            const eyeIcon = this.querySelector('i');
            
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                eyeIcon.className = 'fas fa-eye-slash';
            } else {
                passwordInput.type = 'password';
                eyeIcon.className = 'fas fa-eye';
            }
        });
    });
}

function setupPasswordValidation() {
    const passwordInput = document.getElementById('edit-password');
    const confirmPasswordInput = document.getElementById('edit-confirm-password');
    const messageElement = document.querySelector('.password-match-message');
    
    if (!passwordInput || !confirmPasswordInput || !messageElement) {
        return;
    }
    
    function validatePasswords() {
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;
        const saveButton = document.getElementById('saveEdit');
        
        if (confirmPassword === '') {
            messageElement.textContent = '';
            messageElement.className = 'password-match-message';
            if (saveButton) {
                saveButton.disabled = password === '';
            }
            return;
        }
        
        if (password === confirmPassword) {
            messageElement.textContent = '✓ 密码匹配';
            messageElement.className = 'password-match-message match';
            if (saveButton) {
                saveButton.disabled = false;
            }
        } else {
            messageElement.textContent = '✗ 密码不匹配';
            messageElement.className = 'password-match-message mismatch';
            if (saveButton) {
                saveButton.disabled = true;
            }
        }
    }
    
    passwordInput.addEventListener('input', validatePasswords);
    confirmPasswordInput.addEventListener('input', validatePasswords);
}

function testConnection(type) {
    if (!currentUser) {
        alert('请先登录');
        return;
    }
    
    const button = type === 'BMC' 
        ? document.getElementById('test-bmc-connection') 
        : document.getElementById('test-os-connection');
    
    if (!button) return;
    
    const originalHTML = button.innerHTML;
    
    // 显示连接中状态
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 连接中...';
    button.disabled = true;
    
    // 模拟连接测试
    setTimeout(() => {
        // 随机成功或失败（模拟）
        const isSuccess = Math.random() > 0.3;
        
        const statusBadge = type === 'BMC' 
            ? document.querySelector('#edit-bmc').closest('.info-card').querySelector('.status-badge')
            : document.querySelector('#edit-os').closest('.info-card').querySelector('.status-badge');
        
        if (isSuccess) {
            button.innerHTML = '<i class="fas fa-check-circle"></i> 连接成功';
            
            if (statusBadge) {
                statusBadge.textContent = '已连接';
                statusBadge.className = 'status-badge connected';
            }
        } else {
            button.innerHTML = '<i class="fas fa-times-circle"></i> 连接失败';
            
            if (statusBadge) {
                statusBadge.textContent = '连接失败';
                statusBadge.className = 'status-badge disconnected';
            }
        }
        
        // 3秒后恢复原状
        setTimeout(() => {
            button.innerHTML = originalHTML;
            button.disabled = false;
        }, 3000);
    }, 1500);
}