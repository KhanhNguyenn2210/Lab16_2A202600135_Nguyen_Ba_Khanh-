#  Delivery Checklist — Day 12 Lab Submission

> **Student Name:** Nguyễn Bá Khánh  
> **Student ID:** 2A202600135  
> **Date:** 17/4/2026

---

##  Submission Requirements

Submit a **GitHub repository** containing:

### 1. Mission Answers (40 points)

Create a file `MISSION_ANSWERS.md` with your answers to all exercises:

```markdown
# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found
1. **Hardcoded Secrets**: API Key (`OPENAI_API_KEY`) và Database URL được ghi trực tiếp trong mã nguồn.
2. **Thiếu Config Management**: Các tham số cấu hình như `DEBUG`, `MAX_TOKENS` bị gán cứng thay vì đọc từ biến môi trường.
3. **Insecure Logging**: Sử dụng lệnh `print` thay vì thư viện logging chuyên nghiệp, đồng thời in cả mã bí mật (API Key) ra log.
4. **Thiếu Health Check endpoints**: Không có các endpoint `/health` hay `/ready` để hệ thống giám sát (như Railway/Docker) kiểm tra trạng thái ứng dụng.
5. **Fixed Host/Port**: Gán cứng `host="localhost"` và `port=8000` khiến ứng dụng không thể chạy trong Docker hoặc các nền tảng Cloud yêu cầu port động.

### Exercise 1.2: 
Chạy http://localhost:8000 hiện dòng chữ : {"message":"Hello! Agent is running on my machine :)"}

### Exercise 1.3: Comparison table
`{"app":"AI Agent","version":"1.0.0","environment":"development","status":"running"}`

| Feature | Develop | Production | Why Important? |
|---------|---------|------------|----------------|
| Config  | Hardcoded trong code (API Key, DB) | Đọc từ Environment Variables (.env) | Bảo mật thông tin nhạy cảm và dễ thay đổi cấu hình mà không cần sửa code. |
| Logging | Dùng lệnh `print()` thô | Structured JSON Logging | Giúp các hệ thống giám sát dễ dàng parse và phân tích dữ liệu log. |
| Host/Port | Cố định `localhost:8000` | Bind `0.0.0.0` và nhận Port từ env | Bắt buộc để có thể truy cập được từ bên ngoài container và chạy trên Cloud. |
| Monitoring | Không có cơ chế kiểm tra | Có endpoint `/health` và `/ready` | Giúp Load Balancer và Cloud Platform biết ứng dụng có đang sống hay không. |
| Lifecycle | Tắt ngay lập tức khi ngắt | Graceful Shutdown (Xử lý SIGTERM) | Tránh mất dữ liệu hoặc lỗi khi app đang xử lý dở dang một request thì bị tắt. |
## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. Base image: `python:3.11`
2. Working directory: `/app`

1. **Base image là gì?** Là môi trường nền tảng chứa hệ điều hành và các công cụ cần thiết (ở đây là Python 3.11) để ứng dụng có thể chạy được.
2. **Working directory là gì?** Là thư mục làm việc mặc định bên trong container. Mọi lệnh tiếp theo (COPY, RUN, CMD) sẽ diễn ra tại thư mục này.
3. **Tại sao COPY requirements.txt trước?** Tối ưu hóa layer cache của Docker. Nếu file requirements không đổi, Docker sẽ bỏ qua bước cài đặt thư viện (`pip install`), giúp việc build lại image nhanh hơn rất nhiều khi bạn chỉ thay đổi code.
4. **CMD vs ENTRYPOINT khác nhau thế nào?** `CMD` định nghĩa lệnh mặc định và có thể bị người dùng thay thế khi chạy image. `ENTRYPOINT` định nghĩa lệnh thực thi chính, thường dùng để biến container thành một file thực thi duy nhất.

### Exercise 2.2: Multi-stage build
IMAGE              ID             DISK USAGE   CONTENT SIZE   EXTRA
my-agent:develop   b2872cfc1647       1.66GB          424MB    U 

### Exercise 2.3: Image size comparison
- Develop: 1.66GB
- Production: 236MB
- Difference: ~80 %
IMAGE               ID             DISK USAGE   CONTENT SIZE   EXTRA
my-agent:advanced   59...        236MB         56.6MB
my-agent:develop    b2...      1.66GB          424MB    U 

### Exercise 2.4: Docker Compose stack

**Kiến trúc hệ thống (Architecture Diagram):**

```mermaid
graph TD
    User([User/Client]) -->|Port 80| Nginx[Nginx - Reverse Proxy/Load Balancer]
    Nginx -->|Proxy Pass| Agent[Agent - FastAPI]
    Agent -->|Session/Rate Limit| Redis[(Redis)]
    Agent -->|Vector Search/RAG| Qdrant[(Qdrant)]
```

**Các dịch vụ được khởi tạo:**
1.  **agent**: Đóng vai trò là bộ não xử lý AI (FastAPI).
2.  **redis**: Dùng làm cache để tăng tốc độ truy cập và quản lý giới hạn tần suất gọi API (Rate limiting).
3.  **qdrant**: Cơ sở dữ liệu vector để lưu trữ các đoạn văn bản phục vụ cho tìm kiếm ngữ nghĩa (RAG).
4.  **nginx**: Là cổng vào duy nhất, giúp bảo mật và phân phối các yêu cầu đến các instance của Agent.

**Cách các dịch vụ giao tiếp:**
*   **External**: Người dùng chỉ có thể truy cập qua Port 80 của Nginx.
*   **Internal**: Các dịch vụ giao tiếp với nhau qua một mạng ảo nội bộ của Docker (`bridge network`). Agent kết nối với Redis và Qdrant thông qua tên dịch vụ được định nghĩa trong file compose.

**Kết quả Test:**
1.  **Health check**: `curl http://localhost/health` -> Trả về thông tin trạng thái ứng dụng.
2.  **Agent endpoint**: `curl http://localhost/ask` -> Nhận được phản hồi từ AI Agent thông qua proxy Nginx.
## Part 3: Cloud Deployment

### Exercise 3.1: Railway deployment
- URL: https://your-app.railway.app
- Screenshot: [Link to screenshot in repo]

## Part 4: API Security

### Exercise 4.1-4.3: Test results

#### **1. API Key Authentication (Exercise 4.1)**
 **Lệnh (Sai/Thiếu Key):**
(base) PS K:\VIN_AI\Buoi_12\Lab12-2A202600135-NguyenBaKhanh> curl.exe http://localhost:8000/ask -X POST -H "Content-Type: application/json" -d "{\"question\": \"Hello\"}"
{"detail":"Missing API key. Include header: X-API-Key: <your-key>"}curl: (3) URL rejected: Malformed input to a URL function


- **Kết quả:** `{"detail":"Missing API key. Include header: X-API-Key: <your-key>"}` (HTTP 401)
- **Lệnh (Đúng Key):** `(base) PS K:\VIN_AI\Buoi_12\Lab12-2A202600135-NguyenBaKhanh> Invoke-RestMethod -Uri "http://localhost:8000/ask" -Method Post -Headers @{"X-API-Key"="demo-key-change-in-production"} -ContentType "application/json" -Body '{"question": "Hello AI"}'`

question answer
-------- ------
Hello AI Agent Äang hoáº¡t Äá»ng tá»t! (mock response) Há»i thÃªm cÃ¢u há»i Äi nhÃ©.

- **Kết quả:** `{Hello AI Agent Äang hoáº¡t Äá»ng tá»t! (mock response) Há»i thÃªm cÃ¢u há»i Äi nhÃ©.}` (HTTP 200)

#### **2. JWT Authentication (Exercise 4.2)**
- **Bước 1 (Login):**`$response = Invoke-RestMethod -Uri "http://localhost:8000/auth/token" -Method Post -ContentType "application/json" -Body '{"username": "student", "password": "demo123"}'`
`$token = $response.access_token`
`$token`

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHVkZW50Iiwicm9sZSI6InVzZXIiLCJpYXQiOjE3NzY0MTczMzksImV4cCI6MTc3NjQyMDkzOX0.NREy5YXKKWsTKpPscZxfK8rwKUTaz5AmP4VHmZ_6z3Y
- **Bước 2 (Gửi Token):**   `(base) PS K:\VIN_AI\Buoi_12\Lab12-2A202600135-NguyenBaKhanh> Invoke-RestMethod -Uri "http://localhost:8000/ask" -Method Post -Headers @{"Authorization"="Bearer $token"} -ContentType "application/json" -Body '{"question": "Explain JWT"}'`

question    answer                                                                                     usage
--------    ------                                                                                     -----
Explain JWT TÃ´i lÃ  AI agent ÄÆ°á»£c deploy lÃªn cloud. CÃ¢u há»i cá»§a báº¡n ÄÃ£ ÄÆ°á»£c nháº­n. @{requests_remaining=9; budget_remaining_usd=1.9E-05}


#### **3. Rate Limiting (Exercise 4.3)**
- **Thực hiện:** Gọi API liên tục 20  lần bằng script.
- **Kết quả:**

(base) PS K:\VIN_AI\Buoi_12\Lab12-2A202600135-NguyenBaKhanh> for ($i=1; $i -le 20; $i++) {
>>     Write-Host "Request lần thứ $i..."
>>     try {
>>         Invoke-RestMethod -Uri "http://localhost:8000/ask" -Method Post -Headers @{"Authorization"="Bearer $token"} -ContentType "application/json" -Body "{`"question`": `"Test request
 $i`"}"
>>     } catch {
>>         $_.Exception.Response.StatusCode
>>         $_.Exception.Message
>>         break # Dừng lại khi gặp lỗi (thường là lỗi 429)
>>     }
>> }
Request lần thứ 1...

Request lần thứ 2...
Request lần thứ 3...
Request lần thứ 4...
question       answer                                                                             usage
--------       ------                                                                             -----
Test request 1 Agent Äang hoáº¡t Äá»ng tá»t! (mock response) Há»i thÃªm cÃ¢u há»i Äi nhÃ©. @{requests_remaining=9; budget_remaining_usd=1.6E-05}
Test request 2 Agent Äang hoáº¡t Äá»ng tá»t! (mock response) Há»i thÃªm cÃ¢u há»i Äi nhÃ©. @{requests_remaining=8; budget_remaining_usd=3.3E-05}
Test request 3 Agent Äang hoáº¡t Äá»ng tá»t! (mock response) Há»i thÃªm cÃ¢u há»i Äi nhÃ©. @{requests_remaining=7; budget_remaining_usd=4.9E-05}
Test request 4 Agent Äang hoáº¡t Äá»ng tá»t! (mock response) Há»i thÃªm cÃ¢u há»i Äi nhÃ©. @{requests_remaining=6; budget_remaining_usd=6.6E-05}
Request lần thứ 5...
Test request 5 Agent Äang hoáº¡t Äá»ng tá»t! (mock response) Há»i thÃªm cÃ¢u há»i Äi nhÃ©. @{requests_remaining=5; budget_remaining_usd=8.2E-05}
Request lần thứ 6...
Test request 6 ÄÃ¢y lÃ  cÃ¢u tráº£ lá»i tá»« AI agent (mock). Trong production, ÄÃ¢y sáº½ l... @{requests_remaining=4; budget_remaining_usd=0.000...
Request lần thứ 7...
Test request 7 Agent Äang hoáº¡t Äá»ng tá»t! (mock response) Há»i thÃªm cÃ¢u há»i Äi nhÃ©. @{requests_remaining=3; budget_remaining_usd=0.00012}
Request lần thứ 8...
Test request 8 TÃ´i lÃ  AI agent ÄÆ°á»£c deploy lÃªn cloud. CÃ¢u há»i cá»§a báº¡n ÄÃ£ ÄÆ°á... @{requests_remaining=2; budget_remaining_usd=0.000...
Request lần thứ 9...
Test request 9 Agent Äang hoáº¡t Äá»ng tá»t! (mock response) Há»i thÃªm cÃ¢u há»i Äi nhÃ©. @{requests_remaining=1; budget_remaining_usd=0.000...
Request lần thứ 10...
Test reques... Agent Äang hoáº¡t Äá»ng tá»t! (mock response) Há»i thÃªm cÃ¢u há»i Äi nhÃ©. @{requests_remaining=0; budget_remaining_usd=0.000...
Request lần thứ 11...
429


`The remote server returned an error: (429) Too Many Requests.`


- **Ý nghĩa:** Bảo vệ tài nguyên server và tránh lãng phí chi phí API LLM.

### Exercise 4.4: Cost guard implementation
(base) PS K:\VIN_AI\Buoi_12\Lab12-2A202600135-NguyenBaKhanh> for ($i=1; $i -le 5; $i++) {
>>     Write-Host "Request lần thứ $i..."
>>     try {
>>         Invoke-RestMethod -Uri "http://localhost:8000/ask" -Method Post -Headers @{"Authorization"="Bearer $token"} -ContentType "application/json" -Body "{`"question`": `"Test budget $i`"}"
>>     } catch {
>>         $_.Exception.Response.StatusCode # Sẽ hiện lỗi 402
>>         $_.Exception.Message
>>         break
>>     }
>> }
Request lần thứ 1...

Request lần thứ 2...
Request lần thứ 3...
Request lần thứ 4...
question      answer                                                                                                            usage
--------      ------                                                                                                            -----
Test budget 1 TÃ´i lÃ  AI agent ÄÆ°á»£c deploy lÃªn cloud. CÃ¢u há»i cá»§a báº¡n ÄÃ£ ÄÆ°á»£c nháº­n.                        @{requests_remaining=4; budget_remain...     
Test budget 2 Agent Äang hoáº¡t Äá»ng tá»t! (mock response) Há»i thÃªm cÃ¢u há»i Äi nhÃ©.                                @{requests_remaining=3; budget_remain...        
Test budget 3 ÄÃ¢y lÃ  cÃ¢u tráº£ lá»i tá»« AI agent (mock). Trong production, ÄÃ¢y sáº½ lÃ  response tá»« OpenAI/Anthropic. @{requests_remaining=2; budget_remain...    
Test budget 4 ÄÃ¢y lÃ  cÃ¢u tráº£ lá»i tá»« AI agent (mock). Trong production, ÄÃ¢y sáº½ lÃ  response tá»« OpenAI/Anthropic. @{requests_remaining=1; budget_remain...    
Request lần thứ 5...
Test budget 5 TÃ´i lÃ  AI agent ÄÆ°á»£c deploy lÃªn cloud. CÃ¢u há»i cá»§a báº¡n ÄÃ£ ÄÆ°á»£c nháº­n.                        @{requests_remaining=0; budget_remain...

`request tiếp theo (lần thứ 6 hoặc 7) chắc chắn sẽ bị chặn đứng với mã lỗi 402 (Payment Required).`

- [x] Implement API key authentication
- [x] Hiểu JWT flow
- [x] Implement rate limiting
- [x] Implement cost guard với Redis


## Part 5: Scaling & Reliability



### Exercise 5.1-5.5: Implementation notes
[Your explanations and test results]
```

## Exercise 5.1

(base) PS K:\VIN_AI\Buoi_12\Lab12-2A202600135-NguyenBaKhanh\05-scaling-reliability\develop> Invoke-RestMethod -Uri "http://localhost:8000/health"


status         : ok
uptime_seconds : 10.0
version        : 1.0.0
environment    : development
timestamp      : 2026-04-17T09:33:53.848355+00:00
checks         : @{memory=}

 PS K:\VIN_AI\Buoi_12\Lab12-2A202600135-NguyenBaKhanh> Invoke-RestMethod -Uri "http://localhost:8000/ready"

ready in_flight_requests
----- ------------------
 True                  1

## Exercise 5.2
PS K:\VIN_AI\Buoi_12\Lab12-2A202600135-NguyenBaKhanh> Invoke-RestMethod -Uri "http://localhost:8000/ask?question=Chuyen_gia_AI_la_gi" -Method Post

answer
------
TÃ´i lÃ  AI agent ÄÆ°á»£c deploy lÃªn cloud. CÃ¢u há»i cá»§a báº¡n ÄÃ£ ÄÆ°á»£c nháº­n.
---
 Server sẽ không tắt ngay mà hiện log: Waiting for 1 in-flight requests...



## Exercise 5.4
(base) PS K:\VIN_AI\Buoi_12\Lab12-2A202600135-NguyenBaKhanh\02-docker\production> docker compose up --scale agent=3 -d
time="2026-04-17T17:00:00+07:00" level=warning msg="K:\\VIN_AI\\Buoi_12\\Lab12-2A202600135-NguyenBaKhanh\\02-docker\\production\\docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
[+] up 6/6
 ✔ Container production-redis-1  Healthy                                                                                                                             1.3s
 ✔ Container production-qdrant-1 Started                                                                                                                             0.8s
 ✔ Container production-agent-3  Started                                                                                                                             0.3s
 ✔ Container production-agent-2  Started                                                                                                                             0.3s
 ✔ Container production-agent-1  Started                                                                                                                             0.3s
 ✔ Container production-nginx-1  Started       

 ` chirnh sua mot chut o file production\docker-compose.yml `

### 2. Full Source Code - Lab 06 Complete (60 points)

Your final production-ready agent with all files:

```
your-repo/
├── app/
│   ├── main.py              # Main application
│   ├── config.py            # Configuration
│   ├── auth.py              # Authentication
│   ├── rate_limiter.py      # Rate limiting
│   └── cost_guard.py        # Cost protection
├── utils/
│   └── mock_llm.py          # Mock LLM (provided)
├── Dockerfile               # Multi-stage build
├── docker-compose.yml       # Full stack
├── requirements.txt         # Dependencies
├── .env.example             # Environment template
├── .dockerignore            # Docker ignore
├── railway.toml             # Railway config (or render.yaml)
└── README.md                # Setup instructions
```

**Requirements:**
-  All code runs without errors
-  Multi-stage Dockerfile (image < 500 MB)
-  API key authentication
-  Rate limiting (10 req/min)
-  Cost guard ($10/month)
-  Health + readiness checks
-  Graceful shutdown
-  Stateless design (Redis)
-  No hardcoded secrets

---

### 3. Service Domain Link

Create a file `DEPLOYMENT.md` with your deployed service information:

```markdown
# Deployment Information

## Public URL
https://your-agent.railway.app

## Platform
Railway / Render / Cloud Run

## Test Commands

### Health Check
```bash
curl https://your-agent.railway.app/health
# Expected: {"status": "ok"}
```

### API Test (with authentication)
```bash
curl -X POST https://your-agent.railway.app/ask \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "question": "Hello"}'
```

## Environment Variables Set
- PORT
- REDIS_URL
- AGENT_API_KEY
- LOG_LEVEL

## Screenshots
- [Deployment dashboard](screenshots/dashboard.png)
- [Service running](screenshots/running.png)
- [Test results](screenshots/test.png)
```

##  Pre-Submission Checklist

- [ ] Repository is public (or instructor has access)
- [ ] `MISSION_ANSWERS.md` completed with all exercises
- [ ] `DEPLOYMENT.md` has working public URL
- [ ] All source code in `app/` directory
- [ ] `README.md` has clear setup instructions
- [ ] No `.env` file committed (only `.env.example`)
- [ ] No hardcoded secrets in code
- [ ] Public URL is accessible and working
- [ ] Screenshots included in `screenshots/` folder
- [ ] Repository has clear commit history

---

##  Self-Test

Before submitting, verify your deployment:

```bash
# 1. Health check
curl https://your-app.railway.app/health

# 2. Authentication required
curl https://your-app.railway.app/ask
# Should return 401

# 3. With API key works
curl -H "X-API-Key: YOUR_KEY" https://your-app.railway.app/ask \
  -X POST -d '{"user_id":"test","question":"Hello"}'
# Should return 200

# 4. Rate limiting
for i in {1..15}; do 
  curl -H "X-API-Key: YOUR_KEY" https://your-app.railway.app/ask \
    -X POST -d '{"user_id":"test","question":"test"}'; 
done
# Should eventually return 429
```

---

##  Submission

**Submit your GitHub repository URL:**

```
https://github.com/your-username/day12-agent-deployment
```

**Deadline:** 17/4/2026

---

##  Quick Tips

1.  Test your public URL from a different device
2.  Make sure repository is public or instructor has access
3.  Include screenshots of working deployment
4.  Write clear commit messages
5.  Test all commands in DEPLOYMENT.md work
6.  No secrets in code or commit history

---

##  Need Help?

- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Review [CODE_LAB.md](CODE_LAB.md)
- Ask in office hours
- Post in discussion forum

---

**Good luck! **
