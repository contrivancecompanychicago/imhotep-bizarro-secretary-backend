<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>IMHOTEP Bizarros Medical Secretary</title>
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body>
    <div class="container">
      <header class="topbar">
        <h1>IMHOTEP Bizarros</h1>
        <p>Virtual Lab & Clinic Assistant</p>
      </header>

      <section class="card">
        <h2>1) Staff Login</h2>
        <form id="loginForm">
          <div class="grid">
            <input id="loginEmail" type="email" placeholder="Email" required />
            <input id="loginPassword" type="password" placeholder="Password" required />
          </div>
          <button type="submit">Login</button>
        </form>
      </section>

      <section class="card">
        <h2>2) Create Provider</h2>
        <form id="providerForm">
          <div class="grid">
            <input id="providerName" type="text" placeholder="Provider name" required />
            <input id="providerSpecialty" type="text" placeholder="Specialty" />
            <input id="providerEmail" type="email" placeholder="Provider email" />
          </div>
          <button type="submit">Save Provider</button>
        </form>
      </section>

      <section class="card">
        <h2>3) Patient Intake</h2>
        <form id="patientForm">
          <div class="grid">
            <input id="firstName" type="text" placeholder="First name" required />
            <input id="lastName" type="text" placeholder="Last name" required />
            <input id="dob" type="date" placeholder="Date of birth" />
            <input id="sex" type="text" placeholder="Sex" />
            <input id="phone" type="tel" placeholder="Phone" />
            <input id="email" type="email" placeholder="Email" />
          </div>

          <div class="grid intake-extra">
            <textarea id="symptoms" placeholder="Symptoms / reason for visit"></textarea>
            <select id="triageStatus">
              <option value="pending">Pending</option>
              <option value="non_urgent">Non-urgent</option>
              <option value="urgent">Urgent</option>
              <option value="emergency">Emergency</option>
            </select>
          </div>

          <div class="consent-box">
            <label>
              <input id="consentReceived" type="checkbox" />
              Patient consent received
            </label>
            <textarea id="consentText" placeholder="Consent details or notes"></textarea>
          </div>

          <button type="submit">Create Patient</button>
        </form>
      </section>

      <section class="card">
        <h2>4) Schedule Appointment</h2>
        <form id="appointmentForm">
          <div class="grid">
            <input id="patientId" type="number" placeholder="Patient ID" required />
            <input id="providerId" type="number" placeholder="Provider ID" required />
            <input id="scheduledAt" type="datetime-local" required />
            <input id="reason" type="text" placeholder="Reason for visit" required />
            <textarea id="appointmentNotes" placeholder="Notes"></textarea>
          </div>
          <button type="submit">Book Appointment</button>
        </form>
      </section>

      <section class="card">
        <h2>5) Add Clinical Note</h2>
        <form id="noteForm">
          <div class="grid">
            <input id="notePatientId" type="number" placeholder="Patient ID" required />
            <input id="noteTitle" type="text" placeholder="Note title" required />
          </div>
          <textarea id="noteContent" rows="5" placeholder="Clinical note content..." required></textarea>
          <button type="submit">Save Note</button>
        </form>
      </section>

      <section class="card">
        <h2>6) Search Notes / Documents</h2>
        <form id="searchForm">
          <div class="search-row">
            <input id="searchQuery" type="text" placeholder="Search symptoms, notes, documents..." required />
            <button type="submit">Search</button>
          </div>
        </form>
        <div id="searchResults" class="results"></div>
      </section>

      <section class="card">
        <h2>7) Current Data</h2>
        <div class="button-row">
          <button id="loadPatientsBtn" type="button">Load Patients</button>
          <button id="loadProvidersBtn" type="button">Load Providers</button>
          <button id="loadAppointmentsBtn" type="button">Load Appointments</button>
        </div>

        <div id="patientsList" class="list-box"></div>
        <div id="providersList" class="list-box"></div>
        <div id="appointmentsList" class="list-box"></div>
      </section>
    </div>

    <script src="app.js"></script>
  </body>
</html>
