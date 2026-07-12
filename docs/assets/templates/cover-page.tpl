<div class="print-cover">

  <div class="print-cover__brand">
    <img
      src="https://assets.sandarc.org/logo/current-logo.png"
      alt="SANDARC VEC"
      class="print-cover__logo"
    >
  </div>

  <div class="print-cover__title-block">
    <div class="print-cover__rule"></div>
    <h1 class="print-cover__title">{{ config.site_name }}</h1>
    <p class="print-cover__subtitle">
      Volunteer Examiner Manual
    </p>
    <p class="print-cover__org">
      San Diego County Amateur Radio Council&nbsp;&middot;&nbsp;Volunteer Examiner Coordinator
    </p>
  </div>

  <div class="print-cover__footer">
    <p class="print-cover__edition">
      Generated <span id="print-cover-date"></span>
      <script>
        document.getElementById("print-cover-date").textContent =
          new Date().toLocaleDateString("en-US", {
            year: "numeric", month: "long", day: "numeric"
          });
      </script>
    </p>
    {% if config.copyright %}
    <p class="print-cover__copyright">{{ config.copyright }}</p>
    {% endif %}
    <p class="print-cover__url">vec.sandarc.org/manual</p>
  </div>

</div>
