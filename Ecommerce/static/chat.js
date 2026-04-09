// // // let socket = io();
// // // let currentRoom = 'General';
// // // let username = document.getElementById('username').textContent;
// // // let roomMessages = {};

// // // // Socket event listeners
// // // socket.on('connect', () => {
// // // 	joinRoom('General');
// // // 	highlightActiveRoom('General');
// // // });

// // // socket.on('message', (data) => {
// // // 	addMessage(
// // // 		data.username,
// // // 		data.msg,
// // // 		data.username === username ? 'own' : 'other'
// // // 	);
// // // });

// // // socket.on('private_message', (data) => {
// // // 	addMessage(data.from, `[Private] ${data.msg}`, 'private');
// // // });

// // // socket.on('status', (data) => {
// // // 	addMessage('System', data.msg, 'system');
// // // });

// // // socket.on('active_users', (data) => {
// // // 	const userList = document.getElementById('active-users');
// // // 	userList.innerHTML = data.users
// // // 		.map(
// // // 			(user) => `
// // //             <div class="user-item" onclick="insertPrivateMessage('${user}')">
// // //                 ${user} ${user === username ? '(you)' : ''}
// // //             </div>
// // //         `
// // // 		)
// // // 		.join('');
// // // });

// // // // Message handling
// // // function addMessage(sender, message, type) {
// // // 	if (!roomMessages[currentRoom]) {
// // // 		roomMessages[currentRoom] = [];
// // // 	}
// // // 	roomMessages[currentRoom].push({ sender, message, type });

// // // 	const chat = document.getElementById('chat');
// // // 	const messageDiv = document.createElement('div');
// // // 	messageDiv.className = `message ${type}`;
// // // 	messageDiv.textContent = `${sender}: ${message}`;

// // // 	chat.appendChild(messageDiv);
// // // 	chat.scrollTop = chat.scrollHeight;
// // // }

// // // function sendMessage() {
// // // 	const input = document.getElementById('message');
// // // 	const message = input.value.trim();

// // // 	if (!message) return;

// // // 	if (message.startsWith('@')) {
// // // 		// Send private message
// // // 		const [target, ...msgParts] = message.substring(1).split(' ');
// // // 		const privateMsg = msgParts.join(' ');

// // // 		if (privateMsg) {
// // // 			socket.emit('message', {
// // // 				msg: privateMsg,
// // // 				type: 'private',
// // // 				target: target,
// // // 			});
// // // 		}
// // // 	} else {
// // // 		// Send room message
// // // 		socket.emit('message', {
// // // 			msg: message,
// // // 			room: currentRoom,
// // // 		});
// // // 	}

// // // 	input.value = '';
// // // 	input.focus();
// // // }

// // // function joinRoom(room) {
// // // 	socket.emit('leave', { room: currentRoom });
// // // 	currentRoom = room;
// // // 	socket.emit('join', { room });

// // // 	highlightActiveRoom(room);

// // // 	// Show room history
// // // 	const chat = document.getElementById('chat');
// // // 	chat.innerHTML = '';

// // // 	if (roomMessages[room]) {
// // // 		roomMessages[room].forEach((msg) => {
// // // 			addMessage(msg.sender, msg.message, msg.type);
// // // 		});
// // // 	}
// // // }

// // // function insertPrivateMessage(user) {
// // // 	document.getElementById('message').value = `@${user} `;
// // // 	document.getElementById('message').focus();
// // // }

// // // function handleKeyPress(event) {
// // // 	if (event.key === 'Enter' && !event.shiftKey) {
// // // 		event.preventDefault();
// // // 		sendMessage();
// // // 	}
// // // }

// // // // Initialize chat when page loads
// // // let chat;
// // // document.addEventListener('DOMContentLoaded', () => {
// // // 	chat = new ChatApp();
// // // 	if ('Notification' in window) {
// // // 		Notification.requestPermission();
// // // 	}
// // // });

// // // // Add this new function to handle room highlighting
// // // function highlightActiveRoom(room) {
// // // 	document.querySelectorAll('.room-item').forEach((item) => {
// // // 		item.classList.remove('active-room');
// // // 		if (item.textContent.trim() === room) {
// // // 			item.classList.add('active-room');
// // // 		}
// // // 	});
// // // }









// // let socket = io();

// // let currentRoom = "General";
// // let username = document.getElementById("username").textContent;

// // socket.on("connect", () => {
// //   joinRoom("General");
// // });

// // socket.on("message", (data) => {
// //   addMessage(data.username, data.msg, "other");
// // });

// // socket.on("status", (data) => {
// //   addMessage("System", data.msg, "system");
// // });

// // function addMessage(sender, message, type) {
// //   const chat = document.getElementById("chat");

// //   const div = document.createElement("div");
// //   div.className = `message ${type};`
// //   div.textContent = `${sender}: ${message};`

// //   chat.appendChild(div);
// //   chat.scrollTop = chat.scrollHeight;
// // }

// // function sendMessage() {
// //   const input = document.getElementById("message");
// //   const msg = input.value.trim();

// //   if (!msg) return;

// //   socket.emit("message", {
// //     msg: msg,
// //     room: currentRoom,
// //   });

// //   input.value = "";
// // }

// // function joinRoom(room) {
// //   socket.emit("join", { room });
// //   currentRoom = room;

// //   document.getElementById("chat").innerHTML = "";
// // }

// // function handleKeyPress(e) {
// //   if (e.key === "Enter") {
// //     sendMessage();
// //   }
// // }



// let socket = io();

// let currentRoom = "General";
// let username = document.getElementById("username").textContent;
// let roomMessages = {};

// // ================= SOCKET EVENTS =================

// socket.on("connect", () => {
//   joinRoom("General");
//   highlightActiveRoom("General");
// });

// socket.on("message", (data) => {
//   addMessage(
//     data.username,
//     data.msg,
//     data.username === username ? "own" : "other"
//   );
// });

// socket.on("private_message", (data) => {
//   addMessage(data.from, [Private] ${data.msg}, "private");
// });

// socket.on("status", (data) => {
//   addMessage("System", data.msg, "system");
// });

// socket.on("active_users", (data) => {
//   const userList = document.getElementById("active-users");

//   userList.innerHTML = data.users
//     .map(
//       (user) => 
//         <div class="user-item" onclick="insertPrivateMessage('${user}')">
//           ${user} ${user === username ? "(you)" : ""}
//         </div>
      
//     )
//     .join("");
// });

// // ================= MESSAGE HANDLING =================

// function addMessage(sender, message, type) {
//   if (!roomMessages[currentRoom]) {
//     roomMessages[currentRoom] = [];
//   }

//   roomMessages[currentRoom].push({ sender, message, type });

//   const chat = document.getElementById("chat");

//   const messageDiv = document.createElement("div");
//   messageDiv.className = message ${type};   // ✅ fix
//   messageDiv.textContent = ${sender}: ${message}; // ✅ fix

//   chat.appendChild(messageDiv);
//   chat.scrollTop = chat.scrollHeight;
// }

// // ================= SEND MESSAGE =================

// function sendMessage() {
//   const input = document.getElementById("message");
//   const message = input.value.trim();

//   if (!message) return;

//   if (message.startsWith("@")) {
//     // private message
//     const [target, ...msgParts] = message.substring(1).split(" ");
//     const privateMsg = msgParts.join(" ");

//     if (privateMsg) {
//       socket.emit("message", {
//         msg: privateMsg,
//         type: "private",
//         target: target,
//       });
//     }
//   } else {
//     socket.emit("message", {
//       msg: message,
//       room: currentRoom,
//     });
//   }

//   input.value = "";
//   input.focus();
// }

// // ================= ROOMS =================

// function joinRoom(room) {
//   socket.emit("leave", { room: currentRoom });

//   currentRoom = room;

//   socket.emit("join", { room });

//   highlightActiveRoom(room);

//   const chat = document.getElementById("chat");
//   chat.innerHTML = "";

//   // restore history
//   if (roomMessages[room]) {
//     roomMessages[room].forEach((msg) => {
//       const div = document.createElement("div");
//       div.className = message ${msg.type};
//       div.textContent = ${msg.sender}: ${msg.message};
//       chat.appendChild(div);
//     });
//   }
// }

// // ================= PRIVATE =================

// function insertPrivateMessage(user) {
//   document.getElementById("message").value = @${user} ;
//   document.getElementById("message").focus();
// }

// // ================= INPUT =================

// function handleKeyPress(event) {
//   if (event.key === "Enter" && !event.shiftKey) {
//     event.preventDefault();
//     sendMessage();
//   }
// }

// // ================= UI =================

// function highlightActiveRoom(room) {
//   document.querySelectorAll(".room-item").forEach((item) => {
//     item.classList.remove("active-room");

//     if (item.textContent.trim() === room) {
//       item.classList.add("active-room");
//     }
//   });
// }

// // ❌ شيلنا ChatApp لأنه مش موجود
// document.addEventListener("DOMContentLoaded", () => {
//   if ("Notification" in window) {
//     Notification.requestPermission();
//   }
// });



let socket = io();

let currentRoom = "General";
let username = document.getElementById("username").textContent;

// ================= SOCKET =================

socket.on("connect", () => {
  joinRoom("General");
});

socket.on("message", (data) => {
  addMessage(
    data.username,
    data.msg,
    data.username === username ? "own" : "other"
  );
});

socket.on("status", (data) => {
  addMessage("System", data.msg, "system");
});

socket.on("private_message", (data) => {
  addMessage(data.from, `[Private] ${data.msg}`, "private");
});

socket.on("active_users", (data) => {
  const userList = document.getElementById("active-users");

  userList.innerHTML = data.users
    .map(
      (user) => 
        `<div onclick="insertPrivateMessage('${user}')">
          ${user} ${user === username ? "(you)" : ""}
        </div>`
      
    )
    .join("");
});

// ================= FUNCTIONS =================

function addMessage(sender, message, type) {
  const chat = document.getElementById("chat");

  const div = document.createElement("div");
  div.className =` message ${type};`
  div.textContent = `${sender}: ${message}`

  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function sendMessage() {
  const input = document.getElementById("message");
  const message = input.value.trim();

  if (!message) return;

  if (message.startsWith("@")) {
    const [target, ...msgParts] = message.substring(1).split(" ");
    const privateMsg = msgParts.join(" ");

    if (privateMsg) {
      socket.emit("message", {
        msg: privateMsg,
        type: "private",
        target: target,
      });
    }
  } else {
    socket.emit("message", {
      msg: message,
      room: currentRoom,
    });
  }

  input.value = "";
}

function joinRoom(room) {
  socket.emit("leave", { room: currentRoom });

  currentRoom = room;

  socket.emit("join", { room });

  document.getElementById("chat").innerHTML = "";
}

function insertPrivateMessage(user) {
  document.getElementById("message").value = `@${user}` ;
}

function handleKeyPress(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    sendMessage();
  }
}