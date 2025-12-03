$(document).ready(function() {
    // Connect to the WebSocket server
    // The server URL is automatically determined if not specified, but we can be explicit if needed.
    var socket = io();
    
    var currentUser = "{{ nickname }}"; // This won't work in external JS file directly without passing it.
    // We need to get the nickname from the DOM or a global variable.
    // Let's assume the backend passes it or we get it from the page.
    // A better way: <script> var currentUser = "{{ nickname }}"; </script> in HTML.
    // I will fix this by reading it from the UI element I created.
    
    currentUser = $('#current-nickname').text().trim();

    // Join room
    socket.emit('join', {nickname: currentUser});

    // --- Emoji Feature ---
    var emojis = [
        '😀', '😁', '😂', '🤣', '😃', '😄', '😅', '😆', '😉', '😊', '😋', '😎', '😍', '😘', '🥰', '😗', '😙', '😚', 
        '🙂', '🤗', '🤩', '🤔', '🤨', '😐', '😑', '😶', '🙄', '😏', '😣', '😥', '😮', '🤐', '😯', '😪', '😫', '😴', 
        '😌', '😛', '😜', '😝', '🤤', '😒', '😓', '😔', '😕', '🙃', '🤑', '😲', '☹️', '🙁', '😖', '😞', '😟', '😤', 
        '😢', '😭', '😦', '😧', '😨', '😩', '🤯', '😬', '😰', '😱', '🥵', '🥶', '😳', '🤪', '😵', '😡', '😠', '🤬', 
        '😷', '🤒', '🤕', '🤢', '🤮', '🤧', '😇', '🤠', '🤡', '🥳', '🥴', '🥺', '🤥', '🤫', '🤭', '🧐', '🤓', '😈', 
        '👿', '👹', '👺', '💀', '👻', '👽', '🤖', '💩', '😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾', '👍', 
        '👎', '👊', '✊', '🤛', '🤜', '🤞', '✌️', '🤟', '🤘', '👌', '👈', '👉', '👆', '👇', '☝️', '✋', '🤚', '🖐', 
        '🖖', '👋', '🤙', '💪', '🙏', '💍', '💄', '💋', '👄', '👅', '👂', '👃', '👣', '👁', '👀', '🧠', '🦴', '🦷', 
        '🗣', '👤', '👥'
    ];

    var emojiPicker = $('#emoji-picker');
    
    // Populate Emoji Picker
    emojis.forEach(function(emoji) {
        var btn = $('<button>').text(emoji).addClass('hover:bg-gray-100 p-1 rounded text-xl');
        btn.click(function() {
            var input = $('#message-input');
            input.val(input.val() + emoji);
            input.focus();
            emojiPicker.addClass('hidden');
        });
        emojiPicker.append(btn);
    });

    // Toggle Picker
    $('#emoji-btn').click(function(e) {
        e.stopPropagation();
        emojiPicker.toggleClass('hidden');
    });

    // Close Picker on Outside Click
    $(document).click(function(e) {
        if (!$(e.target).closest('#emoji-picker').length && !$(e.target).closest('#emoji-btn').length) {
            emojiPicker.addClass('hidden');
        }
    });

    // Handle System Messages
    socket.on('system_message', function(data) {
        var html = `
            <div class="flex justify-center my-2">
                <span class="text-xs bg-gray-100 text-gray-500 px-3 py-1 rounded-full">
                    ${data.msg}
                </span>
            </div>
        `;
        $('#chat-messages').append(html);
        scrollToBottom();
    });

    // Handle Chat Messages
    socket.on('receive_message', function(data) {
        var isSelf = (data.nickname === currentUser);
        var alignClass = isSelf ? 'justify-end' : 'justify-start';
        var bubbleClass = isSelf ? 'bg-primary text-white message-bubble-right' : 'bg-white message-bubble-left';
        var avatar = isSelf ? 
            `https://ui-avatars.com/api/?name=${data.nickname}&background=A7C7E7&color=fff` : 
            `https://ui-avatars.com/api/?name=${data.nickname}&background=random`;

        var contentHtml = `<p class="text-sm break-words">${data.msg}</p>`;

        // Handle @电影 functionality
        if (data.msg.startsWith('@电影')) {
            var url = data.msg.substring(3).trim(); // Remove '@电影'
            // Simple cleanup if user used brackets as per instruction syntax literal [url]
            if (url.startsWith('[') && url.endsWith(']')) {
                url = url.substring(1, url.length - 1);
            }

            if (url) {
                var videoSrc = 'https://jx.m3u8.tv/jiexi/?url=' + url;
                contentHtml += `
                    <div class="mt-2 overflow-hidden rounded-lg bg-black">
                        <iframe src="${videoSrc}" style="width: 100%; max-width: 400px; height: 400px;" frameborder="0" allowfullscreen></iframe>
                    </div>
                `;
            }
        }

        var html = `
            <div class="flex items-start ${alignClass}">
                ${!isSelf ? `<img src="${avatar}" class="w-8 h-8 rounded-full object-cover mr-2 mt-1 flex-shrink-0">` : ''}
                <div class="max-w-[75%] flex flex-col ${isSelf ? 'items-end' : ''}">
                    <div class="${bubbleClass} p-3 shadow-sm">
                        ${contentHtml}
                    </div>
                    <span class="text-xs text-gray-400 ${isSelf ? 'mr-2' : 'ml-2'} mt-1">
                        ${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                    </span>
                </div>
                ${isSelf ? `<img src="${avatar}" class="w-8 h-8 rounded-full object-cover ml-2 mt-1 flex-shrink-0">` : ''}
            </div>
        `;
        $('#chat-messages').append(html);
        scrollToBottom();

        // Check if this is a self-message that triggers AI
        if (isSelf && data.msg.startsWith('@成小理')) {
            handleAIChat(data.msg);
        }
    });

    // Handle Music Card
    socket.on('receive_music_card', function(payload) {
        var data = payload.data; // {name, url, singer, image}
        var nickname = payload.nickname;
        var avatar = `https://ui-avatars.com/api/?name=${nickname}&background=FF69B4&color=fff`;
        
        // Music Card HTML
        var cardHtml = `
            <div class="flex flex-col bg-white rounded-xl overflow-hidden shadow-md w-64 border border-gray-100">
                <div class="relative h-48 bg-gray-200 group">
                    <img src="${data.image}" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110">
                    <div class="absolute inset-0 bg-black/20 group-hover:bg-black/40 transition-colors flex items-center justify-center">
                         <div class="w-12 h-12 bg-white/90 rounded-full flex items-center justify-center shadow-lg animate-pulse">
                            <i class="fas fa-music text-primary text-xl"></i>
                         </div>
                    </div>
                </div>
                <div class="p-4">
                    <h3 class="font-bold text-dark truncate">${data.name}</h3>
                    <p class="text-xs text-gray-500 mb-3">${data.singer}</p>
                    <audio controls class="w-full h-8" style="outline: none;">
                        <source src="${data.url}" type="audio/mpeg">
                        Your browser does not support the audio element.
                    </audio>
                </div>
            </div>
        `;

        var html = `
            <div class="flex items-start justify-start">
                <img src="${avatar}" class="w-8 h-8 rounded-full object-cover mr-2 mt-1 flex-shrink-0">
                <div class="max-w-[85%] flex flex-col">
                    ${cardHtml}
                    <span class="text-xs text-gray-400 ml-2 mt-1">${nickname} • 刚刚</span>
                </div>
            </div>
        `;
        $('#chat-messages').append(html);
        scrollToBottom();
    });

    // Handle News Card
    socket.on('receive_news_card', function(payload) {
        var newsList = payload.data;
        var nickname = payload.nickname;
        var avatar = `https://ui-avatars.com/api/?name=${nickname}&background=0D8ABC&color=fff`;
        
        var itemsHtml = newsList.map(function(item) {
            return `
                <div class="border-b border-gray-100 last:border-0 py-2 hover:bg-gray-50 transition-colors px-1 rounded">
                    <div class="flex justify-between items-start">
                        <h4 class="font-medium text-sm text-dark mb-1 leading-tight">${item.title}</h4>
                    </div>
                    <p class="text-xs text-gray-500 line-clamp-2 mb-1">${item.digest}</p>
                    <div class="flex items-center text-[10px] text-gray-400">
                        <i class="far fa-clock mr-1"></i>
                        <span>${item.mtime}</span>
                    </div>
                </div>
            `;
        }).join('');

        var cardHtml = `
            <div class="flex flex-col bg-white rounded-xl overflow-hidden shadow-md w-72 md:w-80 border border-gray-100">
                <div class="bg-gradient-to-r from-blue-500 to-blue-400 p-3 flex items-center justify-between text-white">
                    <div class="flex items-center">
                        <i class="fas fa-newspaper mr-2"></i>
                        <h3 class="font-bold text-sm">今日热点新闻</h3>
                    </div>
                    <span class="text-xs bg-white/20 px-2 py-0.5 rounded-full">Top 10</span>
                </div>
                <div class="p-3 max-h-96 overflow-y-auto custom-scrollbar bg-white">
                    ${itemsHtml}
                </div>
            </div>
        `;

        var html = `
            <div class="flex items-start justify-start">
                <img src="${avatar}" class="w-8 h-8 rounded-full object-cover mr-2 mt-1 flex-shrink-0">
                <div class="max-w-[90%] flex flex-col">
                    ${cardHtml}
                    <span class="text-xs text-gray-400 ml-2 mt-1">${nickname} • 刚刚</span>
                </div>
            </div>
        `;
        $('#chat-messages').append(html);
        scrollToBottom();
    });

    // Handle Weather Card
    socket.on('receive_weather_card', function(payload) {
        var weatherInfo = payload.data;
        var nickname = payload.nickname;
        var avatar = `https://ui-avatars.com/api/?name=${nickname}&background=FF8C00&color=fff`;
        
        var city = weatherInfo.city || '未知城市';
        var today = weatherInfo.data && weatherInfo.data.length > 0 ? weatherInfo.data[0] : null;
        
        if (!today) {
            return; // Should handle error better but basic check
        }

        var current = today.real_time_weather && today.real_time_weather.length > 0 ? today.real_time_weather[0] : {};
        var temp = current.temperature || '-';
        var weather = current.weather || '未知';
        var wind = (current.wind_dir || '') + ' ' + (current.wind_speed || '');
        var low = today.low_temp;
        var high = today.high_temp;
        var date = today.date;
        var day = today.day;

        // Simple Icon Logic
        var iconClass = 'fa-cloud-sun';
        if (weather.includes('晴')) iconClass = 'fa-sun text-yellow-400';
        else if (weather.includes('雨')) iconClass = 'fa-cloud-rain text-blue-400';
        else if (weather.includes('雪')) iconClass = 'fa-snowflake text-blue-200';
        else if (weather.includes('云') || weather.includes('阴')) iconClass = 'fa-cloud text-gray-400';
        else if (weather.includes('雷')) iconClass = 'fa-bolt text-yellow-600';
        else if (weather.includes('雾') || weather.includes('霾')) iconClass = 'fa-smog text-gray-300';

        var cardHtml = `
            <div class="flex flex-col bg-white rounded-xl overflow-hidden shadow-md w-64 border border-gray-100">
                <div class="bg-gradient-to-br from-orange-400 to-pink-500 p-4 text-white relative overflow-hidden">
                    <div class="relative z-10">
                        <div class="flex justify-between items-start mb-4">
                            <div>
                                <h3 class="font-bold text-lg flex items-center">
                                    <i class="fas fa-map-marker-alt mr-2 text-xs opacity-75"></i>
                                    ${city}
                                </h3>
                                <p class="text-xs opacity-80">${date} ${day}</p>
                            </div>
                            <div class="text-4xl">
                                <i class="fas ${iconClass}"></i>
                            </div>
                        </div>
                        <div class="flex items-end">
                            <span class="text-5xl font-bold leading-none">${temp}</span>
                            <span class="text-xl mb-1 ml-1">°C</span>
                        </div>
                        <p class="font-medium mt-1">${weather}</p>
                    </div>
                    <!-- Decorative Circle -->
                    <div class="absolute -top-10 -right-10 w-32 h-32 bg-white/10 rounded-full blur-xl"></div>
                </div>
                
                <div class="p-3 bg-white">
                    <div class="flex justify-between items-center text-sm text-gray-600 mb-2">
                        <span><i class="fas fa-temperature-high mr-1 text-red-400"></i> ${high}°C</span>
                        <span><i class="fas fa-temperature-low mr-1 text-blue-400"></i> ${low}°C</span>
                    </div>
                    <div class="flex items-center text-xs text-gray-400 pt-2 border-t border-gray-50">
                        <i class="fas fa-wind mr-2"></i>
                        <span>${wind}</span>
                    </div>
                </div>
            </div>
        `;

        var html = `
            <div class="flex items-start justify-start">
                <img src="${avatar}" class="w-8 h-8 rounded-full object-cover mr-2 mt-1 flex-shrink-0">
                <div class="max-w-[85%] flex flex-col">
                    ${cardHtml}
                    <span class="text-xs text-gray-400 ml-2 mt-1">${nickname} • 刚刚</span>
                </div>
            </div>
        `;
        $('#chat-messages').append(html);
        scrollToBottom();
    });

    // Handle User List Update
    socket.on('update_users', function(users) {
        $('#user-list').empty();
        users.forEach(function(user) {
            var html = `
                <div class="flex items-center p-2 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer">
                    <div class="relative mr-3">
                        <img src="https://ui-avatars.com/api/?name=${user}&background=random" class="w-8 h-8 rounded-full">
                        <span class="absolute bottom-0 right-0 w-2 h-2 bg-success rounded-full border border-white"></span>
                    </div>
                    <span class="text-sm font-medium">${user}</span>
                </div>
            `;
            $('#user-list').append(html);
        });
    });

    // Send Message
    function sendMessage() {
        var msg = $('#message-input').val().trim();
        if (msg) {
            socket.emit('send_message', {nickname: currentUser, message: msg});
            $('#message-input').val('').focus();
        }
    }

    // Handle AI Chat with SSE
    async function handleAIChat(message) {
        // Create a placeholder for AI response
        var aiAvatar = "https://ui-avatars.com/api/?name=成小理&background=FFD700&color=fff";
        var aiMsgId = 'ai-msg-' + Date.now();
        
        var html = `
            <div class="flex items-start justify-start">
                <img src="${aiAvatar}" class="w-8 h-8 rounded-full object-cover mr-2 mt-1 flex-shrink-0">
                <div class="max-w-[75%] flex flex-col">
                    <div class="bg-white message-bubble-left p-3 shadow-sm">
                        <p class="text-sm break-words" id="${aiMsgId}"><span class="animate-pulse">Thinking...</span></p>
                    </div>
                    <span class="text-xs text-gray-400 ml-2 mt-1">成小理 • 刚刚</span>
                </div>
            </div>
        `;
        $('#chat-messages').append(html);
        scrollToBottom();

        try {
            const response = await fetch('/api/chat/ai', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            });

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            const aiMsgElement = document.getElementById(aiMsgId);
            aiMsgElement.innerHTML = ''; // Clear "Thinking..."

            while (true) {
                const { value, done } = await reader.read();
                if (done) break;
                
                const chunk = decoder.decode(value);
                const lines = chunk.split('\n\n');
                
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = line.replace('data: ', '');
                        if (data === '[DONE]') break;
                        if (data.startsWith('Error:')) {
                             aiMsgElement.innerHTML += `<span class="text-red-500">${data}</span>`;
                        } else {
                             aiMsgElement.innerHTML += data; // Append text
                             scrollToBottom(); // Keep scrolling
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Error:', error);
            var aiMsgElement = document.getElementById(aiMsgId);
            if(aiMsgElement) aiMsgElement.innerHTML += `<br><span class="text-red-500">Connection Error.</span>`;
        }
    }

    $('#send-btn').click(sendMessage);

    $('#message-input').keypress(function(e) {
        if(e.which == 13 && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    function scrollToBottom() {
        var chatDiv = document.getElementById("chat-messages");
        chatDiv.scrollTop = chatDiv.scrollHeight;
    }
});
