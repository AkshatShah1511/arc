const SPREADSHEET_ID = "1kKGx45db5j0LtkmLn8Q06dT0mNXV2MH5qRONTWtmweA";
// Must exactly match the sheet/tab name in your Google Sheet (e.g. 'Sheet1', 'ARC extension', etc.)
const SHEET_NAME = "Sheet1";

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "SAVE_DATA") {
    const { email, url } = message.payload;

    chrome.identity.getAuthToken({ interactive: true }, async (token) => {
      if (!token) {
        sendResponse({ success: false, message: "Auth failed" });
        return;
      }

      const timestamp = new Date().toISOString();

      const body = {
        values: [[ "", timestamp, url, email, "NEW" ]]
      };

      try {
        const res = await fetch(
          // Wrap sheet name in quotes in case it has spaces or special chars
          `https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/'${SHEET_NAME}'!A:D:append?valueInputOption=USER_ENTERED`,
          {
            method: "POST",
            headers: {
              "Authorization": `Bearer ${token}`,
              "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
          }
        );

        if (!res.ok) {
          const errorText = await res.text();
          console.error("Sheets API error", res.status, errorText);
          throw new Error(`Sheets API error ${res.status}: ${errorText}`);
        }

        sendResponse({
          success: true,
          message: "Saved to Google Sheets"
        });
      } catch (e) {
        console.error("Failed to write to Sheets", e);
        sendResponse({
          success: false,
          message: `Failed to write to Sheets: ${e.message || e}`
        });
      }
    });

    return true;
  }
});
