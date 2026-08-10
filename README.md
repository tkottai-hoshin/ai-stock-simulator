Step #1 KYC (Identity Verification) 

Before any trading can occur, users must complete a simple Know Your Customer (KYC) form. 

- Full Legal Name
- Email Address
- Date of birth
- Country

Once submitted, the account is marked as verified and trading is unlocked. Demonstrating the identity verification process required by real brokerages. 

<img width="530" height="1120" alt="image" src="https://github.com/user-attachments/assets/d2be3354-de61-4ec0-9fbc-b1f6b0a11f36" />





Step #2 Process Payment

After KYC is complete, users can buy a random AI stock. 

- User clicks *Buy a Random AI Stock for $25*
- Payment is processed through Stripe (test mode)
- Upon successful payment, the system randomly selects an AI Infrastructure stock
- A fractional number of shares is calculated using the live market price from Yahoo Finance

This step represents the funding / payment rail of a brokerage transaction. 

<img width="1338" height="608" alt="image" src="https://github.com/user-attachments/assets/bd7077d1-136f-464b-ac3f-306654db9ec6" />

<img width="1950" height="1028" alt="image" src="https://github.com/user-attachments/assets/ac2cad5a-f3a7-4686-a1a4-86693dab9336" />





Step #3 Settlement

After the payment is confirmed, the trade goes through a simulated post-trade process:

1. Order is routed to a major exchange (Nasdaq, NYSE, Cboe, etc.)
2. A market maker (Citadel Securities, Virtu, Jane Street, etc.) fills the order
3. The trade is submitted to NSCC (DTCC) for clearing
4. Settlement occurs on **T+1** (one business day later)
5. Shares appear as **Settled** in the user’s portfolio

This section demonstrates how ownership of stock is officially transferred and recorded.

<img width="1392" height="1234" alt="image" src="https://github.com/user-attachments/assets/ba75376a-ba23-4041-85e6-19bdc7a47b47" />
