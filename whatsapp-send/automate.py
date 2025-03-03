import os
from playwright.sync_api import expect, sync_playwright

def wait_for_message_confirmation(page, initial_count):
    # Wait for message list to update
    try:
        # Method 1: Locator-based count check
        expect(page.locator('.message-out')).to_have_count(
            initial_count + 1, 
            timeout=20000
        )
    except:
        # Method 2: DOM order verification
        page.locator('.message-out').nth(initial_count).wait_for(
            state='visible',
            timeout=20000
        )

def send_whatsapp_csv(phone_number, csv_path):
    user_data_dir = "./"
    with sync_playwright() as p:
        # Launch browser
        #browser = p.chromium.launch(headless=False)
        browser = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox'
            ]
        )
        #context = browser.new_context()
        #page = context.new_page()
        page = browser.new_page()
        
        # Navigate to WhatsApp Web
        page.goto("https://web.whatsapp.com/")
        print("Scan QR Code within 30 seconds...")
        
        try:
            # Wait for login completion
            page.wait_for_selector('button[title="New chat"]', timeout=30000)
            
            # Open specific chat
            page.goto(f"https://web.whatsapp.com/send?phone={phone_number}")
            
            # Wait for chat to load and attach file
            page.wait_for_selector('button[title="Attach"]', timeout=15000)
            page.click('button[title="Attach"]')
            
            # Handle file upload
            file_input = page.query_selector('input[type="file"]')
            file_input.set_input_files(os.path.abspath(csv_path))
            
            # Send file
            page.wait_for_selector('div[aria-label="Send"]', timeout=5000)
            #messages_before = page.locator('.message-out').count()
            initial_count = page.locator('.message-out').count()
            print(f"initial count is {initial_count}")
            page.click('div[aria-label="Send"]')
            
            # Verify success
            #page.wait_for_selector('span[data-testid="msg-time"]', timeout=10000)
            wait_for_message_confirmation(page, initial_count)
            # Perform send action
            #page.wait_for_function(
            #    """([initialCount]) => {
            #        return document.querySelectorAll('.message-out').length > initialCount
            #    }""", 
            #    timeout=20000,
            #    arg=[messages_before]
            #)

            print("CSV file sent successfully!")

        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            #context.close()
            pass
            browser.close()

# Usage
if __name__ == "__main__":
    send_whatsapp_csv(
        phone_number="12345678",
        csv_path="titles.csv"
    )
