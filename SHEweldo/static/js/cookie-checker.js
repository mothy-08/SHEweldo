function getCookie(name) {
    const cookies = document.cookie.split("; ");
    for (const cookie of cookies) {
      const [cookieName, cookieValue] = cookie.split("=");
      if (cookieName === name) {
        return cookieValue;
      }
    }
    return null;
  }

  const salaryId = getCookie("salary_id");
  const salaryAmount = getCookie("salary_amount");

  if (!salaryId || !salaryAmount) {
    window.location.href = "/employee/submit";
  }
