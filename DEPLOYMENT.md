
`agent-production-2533.up.railway.app`
#  Deployment Information — Day 12 Lab Submission

> **Student Name:** Nguyễn Bá Khánh  
> **Student ID:** 2A202600135  
> **Date:** 17/04/2026
## Platform
Railway
### Health Check

(base) PS K:\VIN_AI\Buoi_12\Lab12-2A202600135-NguyenBaKhanh\06-lab-complete> curl.exe https://agent-production-2533.up.railway.app/health
{"status":"ok","version":"1.0.0","environment":"development","uptime_seconds":246.0}
 
 ##


{"app":"Production AI Agent","version":"1.0.0","environment":"development","endpoints":{"ask":"POST /ask (requires X-API-Key)","health":"GET /health","ready":"GET /ready"}
## Kiem tra key 
(base) PS K:\VIN_AI\Buoi_12\Lab12-2A202600135-NguyenBaKhanh\06-lab-complete> curl.exe -X POST https://agent-production-2533.up.railway.app/ask `
>>   -H "X-API-Key: your_secret_password" `
>>   -H "Content-Type: application/json" `
>>   -d '{\"city\": \"Hanoi\"}'
{"detail":"Invalid or missing API key. Include header: X-API-Key: <key>"}



## Kiem tra cau hoi bat ky
(base) PS K:\VIN_AI\Buoi_12\Lab12-2A202600135-NguyenBaKhanh\06-lab-complete> curl.exe -X POST https://agent-production-2533.up.railway.app/ask `
>>   -H "X-API-Key: dev-key-change-me" `
>>   -H "Content-Type: application/json" `
>>   -d '{\"city\": \"Hanoi\"}'
{"question":"Thời tiết Hanoi thế nào?","answer":"Thời tiết tại Hanoi là 25°C, trời nắng (Dữ liệu Mock vì thiếu API Key).","timestamp":"2026-04-17T11:10:00.618205+00:00","history":[]}