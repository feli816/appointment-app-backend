const state = {
  activeUserId: "owner-1",
  activeTab: "dashboard",
  urgentCounter: 1,
  school: {
    id: "school-1",
    name: "Auto-Ecole Horizon",
    city: "Lyon",
    plan: "Growth - 12 moniteurs max",
    monthlyRevenue: 690,
    fillRate: 82,
  },
  users: [
    { id: "owner-1", role: "owner", name: "Nadia Laurent", email: "nadia@horizon.fr", location: "Lyon 6e" },
    {
      id: "instr-1",
      role: "instructor",
      name: "Karim Bensaid",
      email: "karim@horizon.fr",
      location: "Lyon Part-Dieu",
      workHours: "08:00 - 18:00",
      specialties: ["Code", "Conduite urbaine"],
    },
    {
      id: "instr-2",
      role: "instructor",
      name: "Emma Vidal",
      email: "emma@horizon.fr",
      location: "Villeurbanne",
      workHours: "09:00 - 19:00",
      specialties: ["Conduite rapide", "Preparation examen"],
    },
    {
      id: "student-1",
      role: "student",
      name: "Lucas Martin",
      email: "lucas@email.com",
      location: "Lyon Bellecour",
      progress: 68,
      preferredInstructorIds: ["instr-1", "instr-2"],
    },
    {
      id: "student-2",
      role: "student",
      name: "Sarah Petit",
      email: "sarah@email.com",
      location: "Lyon Part-Dieu",
      progress: 41,
      preferredInstructorIds: ["instr-1"],
    },
  ],
  slots: [
    { id: "slot-1", instructorId: "instr-1", start: "2026-03-16 09:00", end: "2026-03-16 10:00", status: "booked", studentId: "student-1", location: "Agence Lyon 6e" },
    { id: "slot-2", instructorId: "instr-1", start: "2026-03-16 10:30", end: "2026-03-16 11:30", status: "available", studentId: null, location: "Place Bellecour" },
    { id: "slot-3", instructorId: "instr-2", start: "2026-03-16 14:00", end: "2026-03-16 15:00", status: "available", studentId: null, location: "Villeurbanne Charpennes" },
    { id: "slot-4", instructorId: "instr-2", start: "2026-03-17 08:00", end: "2026-03-17 09:00", status: "booked", studentId: "student-2", location: "Meyzieu" },
  ],
  notifications: [
    { id: "notif-1", title: "Rappel de lecon", body: "Lucas a une lecon avec Karim le 16 mars a 09:00.", audience: ["student-1", "instr-1"], type: "reminder" },
    { id: "notif-2", title: "Nouveau creneau libre", body: "Emma a ouvert un creneau a 14:00 demain a Villeurbanne.", audience: ["student-1", "student-2", "owner-1"], type: "availability" },
  ],
  messages: [
    { id: "msg-1", threadId: "thread-1", fromId: "student-1", toId: "instr-1", sentAt: "2026-03-13 11:10", text: "Bonjour Karim, peut-on partir de Bellecour pour la prochaine seance ?" },
    { id: "msg-2", threadId: "thread-1", fromId: "instr-1", toId: "student-1", sentAt: "2026-03-13 11:15", text: "Oui, rendez-vous valide. Je confirme le point de rencontre dans l'application." },
  ],
  progressSkills: [
    { studentId: "student-1", skill: "Demarrage en cote", level: "Valide" },
    { studentId: "student-1", skill: "Stationnement", level: "En cours" },
    { studentId: "student-1", skill: "Insertion autoroute", level: "Valide" },
    { studentId: "student-2", skill: "Controle du vehicule", level: "Valide" },
    { studentId: "student-2", skill: "Priorites", level: "En cours" },
  ],
};

const tabConfig = {
  owner: [
    { id: "dashboard", label: "Pilotage" },
    { id: "users", label: "Utilisateurs" },
    { id: "calendar", label: "Calendrier" },
    { id: "messages", label: "Messages" },
    { id: "billing", label: "Abonnement" },
  ],
  instructor: [
    { id: "dashboard", label: "Journee" },
    { id: "calendar", label: "Calendrier" },
    { id: "students", label: "Eleves" },
    { id: "messages", label: "Messages" },
    { id: "progress", label: "Progression" },
  ],
  student: [
    { id: "dashboard", label: "Accueil" },
    { id: "calendar", label: "Reserver" },
    { id: "bookings", label: "Mes lecons" },
    { id: "messages", label: "Messages" },
    { id: "progress", label: "Progression" },
  ],
};

const el = {
  roleSwitcher: document.querySelector("#role-switcher"),
  schoolSummary: document.querySelector("#school-summary"),
  notificationList: document.querySelector("#notification-list"),
  tabBar: document.querySelector("#tab-bar"),
  mainContent: document.querySelector("#main-content"),
  contextContent: document.querySelector("#context-content"),
  screenTitle: document.querySelector("#screen-title"),
  heroEyebrow: document.querySelector("#hero-eyebrow"),
  heroTitle: document.querySelector("#hero-title"),
  heroCopy: document.querySelector("#hero-copy"),
  urgentBookingButton: document.querySelector("#urgent-booking-button"),
};

function getUser(id = state.activeUserId) {
  return state.users.find((user) => user.id === id);
}

function getRoleLabel(role) {
  return { owner: "Proprietaire", instructor: "Moniteur", student: "Eleve" }[role];
}

function formatSlot(slot) {
  return `${slot.start} - ${slot.end.split(" ")[1]}`;
}

function getInstructorName(id) {
  return getUser(id)?.name ?? "Moniteur inconnu";
}

function getStudentName(id) {
  return getUser(id)?.name ?? "Eleve inconnu";
}

function visibleNotifications() {
  return state.notifications.filter((notif) => notif.audience.includes(state.activeUserId));
}

function activeTabs() {
  return tabConfig[getUser().role];
}

function switchUser(userId) {
  state.activeUserId = userId;
  state.activeTab = "dashboard";
  render();
}

function setTab(tabId) {
  state.activeTab = tabId;
  render();
}

function createBooking(slotId) {
  const user = getUser();
  if (user.role !== "student") return;
  const slot = state.slots.find((item) => item.id === slotId);
  if (!slot || slot.status === "booked") return;

  const alreadyBooked = state.slots.some((item) => item.studentId === user.id && item.start === slot.start && item.status === "booked");
  if (alreadyBooked) {
    state.notifications.unshift({
      id: `notif-${Date.now()}`,
      title: "Reservation refusee",
      body: "Ce creneau chevauche une lecon deja reservee.",
      audience: [user.id],
      type: "warning",
    });
    render();
    return;
  }

  slot.status = "booked";
  slot.studentId = user.id;
  state.notifications.unshift({
    id: `notif-${Date.now()}`,
    title: "Reservation confirmee",
    body: `Votre lecon avec ${getInstructorName(slot.instructorId)} est confirmee le ${slot.start}.`,
    audience: [user.id, slot.instructorId, "owner-1"],
    type: "success",
  });
  render();
}

function releaseSlot(slotId) {
  const slot = state.slots.find((item) => item.id === slotId);
  if (!slot) return;
  slot.status = "available";
  slot.studentId = null;
  state.notifications.unshift({
    id: `notif-${Date.now()}`,
    title: "Creneau libere",
    body: `${getInstructorName(slot.instructorId)} a rouvert le creneau du ${slot.start}.`,
    audience: state.users.filter((user) => user.role === "student").map((user) => user.id),
    type: "availability",
  });
  render();
}

function addInstructorSlot() {
  const user = getUser();
  if (user.role !== "instructor") return;
  state.slots.unshift({
    id: `slot-${Date.now()}`,
    instructorId: user.id,
    start: "2026-03-18 17:30",
    end: "2026-03-18 18:30",
    status: "available",
    studentId: null,
    location: user.location,
  });
  state.notifications.unshift({
    id: `notif-${Date.now() + 1}`,
    title: "Nouvelle disponibilite",
    body: `${user.name} a ajoute un creneau le 18 mars a 17:30.`,
    audience: state.users.filter((item) => item.role !== "instructor").map((item) => item.id),
    type: "availability",
  });
  render();
}

function addUrgentRequest() {
  const user = getUser();
  if (user.role !== "student") {
    state.notifications.unshift({
      id: `notif-${Date.now()}`,
      title: "Mode urgent",
      body: "Passez sur un compte eleve pour tester la reservation immediate geolocalisee.",
      audience: [state.activeUserId],
      type: "warning",
    });
    render();
    return;
  }

  state.notifications.unshift({
    id: `notif-${Date.now()}`,
    title: "Demande urgente envoyee",
    body: `Demande immediate #${state.urgentCounter} envoyee autour de ${user.location}. Moniteurs proches notifies.`,
    audience: [user.id, "instr-1", "instr-2", "owner-1"],
    type: "success",
  });
  state.urgentCounter += 1;
  render();
}

function sendMessage() {
  const user = getUser();
  const target = user.role === "student" ? "instr-1" : "student-1";
  state.messages.push({
    id: `msg-${Date.now()}`,
    threadId: "thread-1",
    fromId: user.id,
    toId: target,
    sentAt: "2026-03-13 16:45",
    text: user.role === "student" ? "Je viens de confirmer ma disponibilite pour un cours supplementaire." : "Creneau ajuste et point de rendez-vous partage dans l'application.",
  });
  render();
}

function statCard(label, value, help) {
  return `<article class="stat-card"><span class="stat-label">${label}</span><strong class="stat-value">${value}</strong><span class="stat-help">${help}</span></article>`;
}

function renderBookingCard(slot) {
  const instructorName = getInstructorName(slot.instructorId);
  const studentName = slot.studentId ? getStudentName(slot.studentId) : "Libre";
  return `<article class="booking-card"><span class="booking-meta">${formatSlot(slot)}</span><strong>${instructorName}</strong><p>Eleve: ${studentName}</p><p>Rendez-vous: ${slot.location}</p></article>`;
}

function renderSlotCard(slot, role) {
  const isBooked = slot.status === "booked";
  const action = role === "student" && !isBooked
    ? `<button class="primary-button" data-book-slot="${slot.id}">Reserver</button>`
    : role === "instructor" && isBooked
      ? `<button class="secondary-button" data-release-slot="${slot.id}">Liberer</button>`
      : "";
  return `<article class="slot-card"><span class="slot-meta">${formatSlot(slot)}</span><strong>${getInstructorName(slot.instructorId)}</strong><p>Lieu: ${slot.location}</p><p>Etat: ${isBooked ? "Reserve" : "Disponible"}</p>${isBooked ? `<p>Eleve: ${getStudentName(slot.studentId)}</p>` : ""}<div class="actions-row">${action}</div></article>`;
}

function bindAction(actionName, handler) {
  const element = document.querySelector(`[data-action="${actionName}"]`);
  if (element) element.addEventListener("click", handler);
}

function bindRepeatedActions(attribute, handler) {
  document.querySelectorAll(`[data-${attribute}]`).forEach((button) => {
    button.addEventListener("click", () => handler(button.dataset[attribute]));
  });
}

function renderRoleSwitcher() {
  el.roleSwitcher.innerHTML = "";
  state.users.forEach((user) => {
    const button = document.createElement("button");
    button.className = `role-button ${user.id === state.activeUserId ? "active" : ""}`;
    button.textContent = `${getRoleLabel(user.role)} - ${user.name.split(" ")[0]}`;
    button.addEventListener("click", () => switchUser(user.id));
    el.roleSwitcher.appendChild(button);
  });
}

function renderSchoolSummary() {
  const instructors = state.users.filter((user) => user.role === "instructor").length;
  const students = state.users.filter((user) => user.role === "student").length;
  el.schoolSummary.innerHTML = `<p><strong>${state.school.name}</strong></p><p>${state.school.city}</p><p>${instructors} moniteurs actifs</p><p>${students} eleves suivis</p><p>Plan ${state.school.plan}</p>`;
}

function renderNotifications() {
  const notifications = visibleNotifications().slice(0, 4);
  el.notificationList.innerHTML = notifications.length
    ? notifications.map((notif) => `<article class="notification-card"><strong>${notif.title}</strong><p>${notif.body}</p></article>`).join("")
    : `<div class="empty-state">Aucune notification pour ce profil.</div>`;
}

function renderTabs() {
  el.tabBar.innerHTML = "";
  activeTabs().forEach((tab) => {
    const button = document.createElement("button");
    button.className = `tab-button ${tab.id === state.activeTab ? "active" : ""}`;
    button.textContent = tab.label;
    button.addEventListener("click", () => setTab(tab.id));
    el.tabBar.appendChild(button);
  });
}

function renderHero() {
  const copy = {
    owner: ["Pilotage multi-tenant", "Suivez le remplissage, les moniteurs et la croissance SaaS", "Le proprietaire pilote l'activite de l'ecole, les comptes, les reservations et l'abonnement depuis un cockpit unique."],
    instructor: ["Journee moniteur", "Ouvrez des creneaux, gerez les eleves et fluidifiez vos tournees", "Le moniteur gere ses disponibilites, ses rendez-vous et la progression sans friction mobile."],
    student: ["Experience eleve", "Reservez vite, suivez vos competences et restez connecte", "L'eleve trouve un moniteur disponible, reserve une lecon et retrouve toutes ses informations au meme endroit."],
  }[getUser().role];
  el.screenTitle.textContent = activeTabs().find((tab) => tab.id === state.activeTab)?.label ?? "DriveSchool";
  el.heroEyebrow.textContent = copy[0];
  el.heroTitle.textContent = copy[1];
  el.heroCopy.textContent = copy[2];
}

function renderOwnerDashboard() {
  const booked = state.slots.filter((slot) => slot.status === "booked").length;
  el.mainContent.innerHTML = `
    <div class="section-header"><h3>Vue globale de l'ecole</h3><span class="pill success">${state.school.fillRate}% de remplissage</span></div>
    <div class="stats-grid">
      ${statCard("Chiffre MRR", `${state.school.monthlyRevenue} EUR`, "Abonnement auto-ecole en cours")}
      ${statCard("Heures reservees", `${booked} h`, "Heures de conduite deja planifiees")}
      ${statCard("Moniteurs actifs", "2", "Tous connectes cette semaine")}
      ${statCard("Eleves en suivi", "2", "Progression moyenne 54%")}
    </div>
    <div class="section-header"><h3>Reservations recentes</h3><span class="pill">${booked}/${state.slots.length} creneaux occupes</span></div>
    <div class="stack">${state.slots.slice(0, 3).map(renderBookingCard).join("")}</div>`;
  el.contextContent.innerHTML = `
    <div class="stack">
      <article class="info-card"><strong>Taux d'occupation</strong><p>Les creneaux du lundi matin sont pleins a 100%. Une campagne dernieres minutes peut optimiser l'apres-midi.</p></article>
      <article class="info-card"><strong>Activite des moniteurs</strong><p>Karim est reserve a 2/2. Emma a 1 creneau libre a pousser en notification.</p></article>
      <article class="info-card"><strong>Options futures</strong><p>Multi-agence, paiement en ligne, CRM leads, scoring de no-show et franchise management.</p></article>
    </div>`;
}

function renderUsersManagement() {
  const instructors = state.users.filter((user) => user.role === "instructor");
  const students = state.users.filter((user) => user.role === "student");
  el.mainContent.innerHTML = `
    <div class="section-header"><h3>Gestion des comptes</h3><button class="primary-button" data-action="simulate-invite">Inviter un moniteur</button></div>
    <div class="split">
      <div><h3>Moniteurs</h3><div class="stack">${instructors.map((user) => `<article class="info-card"><strong>${user.name}</strong><p>${user.email}</p><p>${user.workHours}</p><p>${user.specialties.join(", ")}</p></article>`).join("")}</div></div>
      <div><h3>Eleves</h3><div class="stack">${students.map((user) => `<article class="info-card"><strong>${user.name}</strong><p>${user.email}</p><p>Progression ${user.progress}%</p><p>Moniteurs accessibles: ${user.preferredInstructorIds.map(getInstructorName).join(", ")}</p></article>`).join("")}</div></div>
    </div>`;
  el.contextContent.innerHTML = `<article class="info-card"><strong>Multi-tenant et permissions</strong><p>Chaque compte appartient a une ecole. Les roles limitent la visibilite: ecole globale, moniteur personnel, eleve cible.</p></article>`;
  bindAction("simulate-invite", () => {
    state.notifications.unshift({ id: `notif-${Date.now()}`, title: "Invitation envoyee", body: "Un email d'invitation moniteur a ete prepare pour un nouveau collaborateur.", audience: ["owner-1"], type: "success" });
    render();
  });
}

function renderCalendar() {
  const user = getUser();
  const visibleSlots = user.role === "owner"
    ? state.slots
    : user.role === "instructor"
      ? state.slots.filter((slot) => slot.instructorId === user.id)
      : state.slots.filter((slot) => user.preferredInstructorIds.includes(slot.instructorId) || slot.studentId === user.id);
  el.mainContent.innerHTML = `
    <div class="section-header"><h3>${user.role === "student" ? "Disponibilites a reserver" : "Calendrier des lecons"}</h3>${user.role === "instructor" ? `<button class="primary-button" data-action="add-slot">Ajouter un creneau</button>` : ""}</div>
    <div class="stack">${visibleSlots.map((slot) => renderSlotCard(slot, user.role)).join("")}</div>`;
  el.contextContent.innerHTML = `
    <div class="stack">
      <article class="info-card"><strong>Regles de reservation</strong><p>Le prototype bloque les doubles reservations sur un meme horaire et publie une notification de confirmation.</p></article>
      <article class="info-card"><strong>Geolocalisation</strong><p>Chaque creneau contient un point de rendez-vous. Le mode urgent pousse les moniteurs proches.</p></article>
    </div>`;
  bindAction("add-slot", addInstructorSlot);
  bindRepeatedActions("book-slot", createBooking);
  bindRepeatedActions("release-slot", releaseSlot);
}

function renderMessages() {
  const user = getUser();
  const messages = state.messages.filter((message) => message.fromId === user.id || message.toId === user.id);
  el.mainContent.innerHTML = `
    <div class="section-header"><h3>Messagerie integree</h3><button class="primary-button" data-action="send-message">Envoyer un message demo</button></div>
    <div class="stack">${messages.map((message) => `<article class="message-card"><span class="message-meta">${message.sentAt}</span><strong>${getUser(message.fromId).name} vers ${getUser(message.toId).name}</strong><p>${message.text}</p></article>`).join("")}</div>`;
  el.contextContent.innerHTML = `<article class="info-card"><strong>Evolution cible</strong><p>Threads temps reel via WebSocket, pieces jointes, lecture/non lecture, moderation et templates transactionnels.</p></article>`;
  bindAction("send-message", sendMessage);
}

function renderBilling() {
  el.mainContent.innerHTML = `
    <div class="section-header"><h3>Abonnement SaaS</h3><span class="pill success">Plan actif</span></div>
    <div class="stats-grid">
      ${statCard("Plan", "Growth", "Jusqu'a 12 moniteurs")}
      ${statCard("Facturation", `${state.school.monthlyRevenue} EUR / mois`, "Paiement preleve le 1er")}
      ${statCard("Modules", "Core + Messages", "Notifications incluses")}
      ${statCard("Upsell", "Paiement en ligne", "Pret a activer")}
    </div>`;
  el.contextContent.innerHTML = `<article class="info-card"><strong>Monetisation</strong><p>Base abonnement + palier moniteurs + options premium: SMS, analytics avancees, multi-sites, white-label.</p></article>`;
}

function renderInstructorDashboard() {
  const user = getUser();
  const todaySlots = state.slots.filter((slot) => slot.instructorId === user.id);
  const bookedCount = todaySlots.filter((slot) => slot.status === "booked").length;
  el.mainContent.innerHTML = `
    <div class="section-header"><h3>Planning de ${user.name}</h3><span class="pill success">${bookedCount}/${todaySlots.length} creneaux remplis</span></div>
    <div class="stats-grid">
      ${statCard("Horaires", user.workHours, "Disponibilites configurees")}
      ${statCard("Lecons reservees", `${bookedCount}`, "Pour les 2 prochains jours")}
      ${statCard("Point de depart", user.location, "Geolocalisation activee")}
      ${statCard("Competences suivies", "5", "Saisie rapide par eleve")}
    </div>
    <div class="section-header"><h3>Tournee a venir</h3></div>
    <div class="stack">${todaySlots.map(renderBookingCard).join("")}</div>`;
  el.contextContent.innerHTML = `<article class="info-card"><strong>Actions rapides</strong><p>Ajoutez un creneau, confirmez un point de rendez-vous, envoyez un message ou signalez un retard.</p></article>`;
}

function renderStudentsList() {
  const user = getUser();
  const linkedStudents = state.users.filter((candidate) => candidate.role === "student" && state.slots.some((slot) => slot.instructorId === user.id && slot.studentId === candidate.id));
  el.mainContent.innerHTML = `
    <div class="section-header"><h3>Eleves suivis</h3><span class="pill">${linkedStudents.length} eleves actifs</span></div>
    <div class="stack">${linkedStudents.map((student) => `<article class="progress-card"><strong>${student.name}</strong><p>${student.email}</p><p>Progression ${student.progress}%</p><div class="progress-bar"><div class="progress-fill" style="width:${student.progress}%"></div></div></article>`).join("")}</div>`;
  el.contextContent.innerHTML = `<article class="info-card"><strong>Suivi pedagogique</strong><p>Chaque lecon peut alimenter des competences, observations, objectifs et alertes examen.</p></article>`;
}

function renderProgress() {
  const user = getUser();
  const studentId = user.role === "student" ? user.id : "student-1";
  const student = getUser(studentId);
  const skills = state.progressSkills.filter((entry) => entry.studentId === studentId);
  el.mainContent.innerHTML = `
    <div class="section-header"><h3>Progression de ${student.name}</h3><span class="pill success">${student.progress}% de preparation</span></div>
    <div class="progress-card"><p>Preparation a l'examen pratique</p><div class="progress-bar"><div class="progress-fill" style="width:${student.progress}%"></div></div></div>
    <div class="section-header"><h3>Competences</h3></div>
    <div class="stack">${skills.map((entry) => `<article class="info-card"><strong>${entry.skill}</strong><span class="pill ${entry.level === "Valide" ? "success" : "warning"}">${entry.level}</span></article>`).join("")}</div>`;
  el.contextContent.innerHTML = `<article class="info-card"><strong>Vision produit</strong><p>Le moteur de progression peut ensuite etre mutualise pour d'autres secteurs: coaching, sante, formation, services terrain.</p></article>`;
}

function renderStudentDashboard() {
  const user = getUser();
  const bookings = state.slots.filter((slot) => slot.studentId === user.id);
  const nextFreeSlots = state.slots.filter((slot) => slot.status === "available").slice(0, 2);
  el.mainContent.innerHTML = `
    <div class="section-header"><h3>Bonjour ${user.name.split(" ")[0]}</h3><span class="pill success">${user.progress}% de progression</span></div>
    <div class="stats-grid">
      ${statCard("Lecons planifiees", `${bookings.length}`, "Toutes visibles sur mobile")}
      ${statCard("Moniteurs disponibles", `${user.preferredInstructorIds.length}`, "Selon votre pack")}
      ${statCard("Mode urgent", "Actif", "Recherche locale instantanee")}
      ${statCard("Prochain objectif", "Stationnement", "Competence a valider")}
    </div>
    <div class="section-header"><h3>Prochaines opportunites</h3></div>
    <div class="stack">${nextFreeSlots.map((slot) => renderSlotCard(slot, "student")).join("")}</div>`;
  el.contextContent.innerHTML = `
    <div class="stack">
      <article class="info-card"><strong>Premier rendez-vous</strong><p>Le point de rencontre est partage dans chaque reservation pour fluidifier la premiere lecon.</p></article>
      <article class="info-card"><strong>Derniere minute</strong><p>Le bouton "Disponibilite immediate" simule une demande geolocalisee de cours rapide.</p></article>
    </div>`;
  bindRepeatedActions("book-slot", createBooking);
}

function renderBookings() {
  const user = getUser();
  const bookings = state.slots.filter((slot) => slot.studentId === user.id);
  el.mainContent.innerHTML = `
    <div class="section-header"><h3>Mes lecons reservees</h3><span class="pill">${bookings.length} lecons</span></div>
    <div class="stack">${bookings.length ? bookings.map(renderBookingCard).join("") : `<div class="empty-state">Aucune reservation pour le moment.</div>`}</div>`;
  el.contextContent.innerHTML = `<article class="info-card"><strong>Notifications de rappel</strong><p>Les rappels push peuvent etre programmes a H-24, H-2 et a l'arrivee du moniteur.</p></article>`;
}

function renderMainContent() {
  const route = `${getUser().role}:${state.activeTab}`;
  const map = {
    "owner:dashboard": renderOwnerDashboard,
    "owner:users": renderUsersManagement,
    "owner:calendar": renderCalendar,
    "owner:messages": renderMessages,
    "owner:billing": renderBilling,
    "instructor:dashboard": renderInstructorDashboard,
    "instructor:calendar": renderCalendar,
    "instructor:students": renderStudentsList,
    "instructor:messages": renderMessages,
    "instructor:progress": renderProgress,
    "student:dashboard": renderStudentDashboard,
    "student:calendar": renderCalendar,
    "student:bookings": renderBookings,
    "student:messages": renderMessages,
    "student:progress": renderProgress,
  };
  map[route]?.();
}

function render() {
  renderRoleSwitcher();
  renderSchoolSummary();
  renderNotifications();
  renderTabs();
  renderHero();
  renderMainContent();
}

el.urgentBookingButton.addEventListener("click", addUrgentRequest);
render();
