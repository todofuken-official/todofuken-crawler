import { initializeApp } from "https://www.gstatic.com/firebasejs/10.13.2/firebase-app.js";
import { getMessaging, onBackgroundMessage } from "https://www.gstatic.com/firebasejs/10.13.2/firebase-messaging-sw.js";

const firebaseConfig = {
  apiKey: "AIzaSyAGY3ueFfq0T2ZTCWZxfDPS3pjr3UfsYDA",
  authDomain: "todofuken-crawler.firebaseapp.com",
  projectId: "todofuken-crawler",
  storageBucket: "todofuken-crawler.firebasestorage.app",
  messagingSenderId: "380143421074",
  appId: "1:380143421074:web:87ff4d47ba26a0339c084b"
};

const app = initializeApp(firebaseConfig);

const messaging = getMessaging(app);

onBackgroundMessage(messaging, (payload) => {
  console.log("Background message:", payload);

  const title = payload.notification?.title || "Todofuken 알림";
  const body = payload.notification?.body || "새로운 여행 정보가 도착했습니다.";

  self.registration.showNotification(title, {
    body,
    icon: "/icon.png"
  });
});