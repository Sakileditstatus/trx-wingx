import requests
import json
import time
from datetime import datetime, timezone, timedelta
from flask import Flask, jsonify, request

# Try to import curl_cffi for Cloudflare bypass (works in serverless), fallback to cloudscraper, then requests
USE_CURL_CFFI = False
USE_CLOUDSCRAPER = False

try:
    from curl_cffi import requests as curl_requests  # type: ignore
    USE_CURL_CFFI = True
except ImportError:
    try:
        import cloudscraper  # type: ignore
        USE_CLOUDSCRAPER = True
    except ImportError:
        pass

# Initialize Flask App
app = Flask(__name__)

# --- Configuration ---
API_URL = "https://api.ar-lottery01.com/api/Lottery/GetHistoryIssuePage"
DRAW_API_URL = "https://draw.ar-lottery01.com/TrxWinGo/TrxWinGo_1M.json"
STATS_API_URL = "https://api.ar-lottery01.com/api/Lottery/GetTrendStatistics"
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJUb2tlblR5cGUiOiJBY2Nlc3NfVG9rZW4iLCJUZW5hbnRJZCI6IjEwMTIiLCJVc2VySWQiOiIxMDEyMDAwMDA5NTM5OCIsIkFnZW50Q29kZSI6IjEwMTIwMSIsIlRlbmFudEFjY291bnQiOiI5NTM5OCIsIkxvZ2luSVAiOiIyNDA5OjQwZTE6MTFiNDplZTRjOjNjNjQ6YjRkYTo4YzkzOjhiODEiLCJMb2dpblRpbWUiOiIxNzY1NzE4MTQ4MTIxIiwiU3lzQ3VycmVuY3kiOiJJTlIiLCJTeXNMYW5ndWFnZSI6ImVuIiwiRGV2aWNlVHlwZSI6IlBDIiwiTG90dGVyeUxpbWl0R3JvdXBOdW0iOiIwIiwiVXNlclR5cGUiOiIwIiwibmJmIjoxNzY1NzIwOTg2LCJleHAiOjE3NjU3MjQ1ODYsImlzcyI6Imp3dElzc3VlciIsImF1ZCI6ImxvdHRlcnlUaWNrZXQifQ.mwNCbPyHWIO4w6WMTeWLBY2dlrnljqIqxpSIdR4FtAs"

@app.route('/', methods=['GET'])
def api_documentation():
    """
    API Documentation - Lists all available endpoints and how to use them.
    """
    developer_info = {
        "name": "@nexcoder",
        "contact": "github.com/enzosrs"
    }
    
    server_info = {
        "timestamp": int(time.time()),
        "endpoint": "/",
        "method": "GET",
        "status": "active"
    }
    
    endpoints = {
        "history": {
            "path": "/api/history",
            "method": "GET",
            "params": ["gameCode", "pageNo", "pageSize"],
            "example": "/api/history?gameCode=TrxWinGo_1M&pageNo=1&pageSize=10"
        },
        "iusee": {
            "path": "/api/iusee",
            "method": "GET",
            "params": ["ts"],
            "example": "/api/iusee?ts=1765719395722"
        },
        "stats": {
            "path": "/api/stats",
            "method": "GET",
            "params": ["gameCode", "pageNo", "pageSize"],
            "example": "/api/stats?gameCode=TrxWinGo_1M&pageNo=1&pageSize=10"
        }
    }
    
    response = {
        "developer": developer_info,
        "server": server_info,
        "message": "Lottery API – Available Endpoints",
        "endpoints": endpoints,
        "success": True
    }
    
    return jsonify(response), 200




@app.route('/api/history', methods=['GET'])
def get_lottery_history():
    """
    Fetches lottery history from the external API and returns a clean, structured response.
    Accepts gameCode, pageNo, and pageSize as query parameters.
    """
    # Get Query Parameters
    game_code = request.args.get('gameCode', default="TrxWinGo_1M", type=str)
    page_no = request.args.get('pageNo', default=1, type=int)
    page_size = request.args.get('pageSize', default=10, type=int)
    
    # Use original payload format with static signature (don't change)
    params = {
        "gameCode": game_code,
        "pageNo": page_no,
        "pageSize": page_size,
        "language": "en",
        "random": "822698754231",
        "signature": "480AAF1DE0D41909BB10998F7DFFF3F3",
        "timestamp": "1765718452"
    }
    
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "authorization": f"Bearer {AUTH_TOKEN}",
        "origin": "https://bhtclub2.com",
        "referer": "https://bhtclub2.com/",
        "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "cache-control": "no-cache",
        "pragma": "no-cache"
    }
    
    # Developer info
    developer_info = {
        "name": "@nexcoder",
        "contact": "github.com/enzosrs"
    }
    
    # Server info
    server_info = {
        "timestamp": int(time.time()),
        "endpoint": "/api/history",
        "method": "GET",
        "status": "active"
    }
    
    try:
        # Use curl_cffi for Cloudflare bypass (best for serverless), fallback to cloudscraper, then requests
        if USE_CURL_CFFI:
            # curl_cffi mimics real browser TLS fingerprints to bypass Cloudflare
            response = curl_requests.get(
                API_URL, 
                params=params, 
                headers=headers, 
                timeout=15, 
                allow_redirects=True,
                impersonate="chrome119"  # Mimic Chrome 119 browser
            )
        elif USE_CLOUDSCRAPER:
            scraper = cloudscraper.create_scraper()
            scraper.headers.update(headers)
            response = scraper.get(API_URL, params=params, timeout=15, allow_redirects=True)
        else:
            session = requests.Session()
            session.headers.update(headers)
            response = session.get(API_URL, params=params, timeout=15, allow_redirects=True)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        # Get API response data
        api_data = response.json()
        
        # Return response with developer and server info
        return jsonify({
            "developer": developer_info,
            "server_info": server_info,
            "data": api_data
        }), 200
        
    except requests.exceptions.HTTPError as http_err:
        error_details = "No details available."
        error_message = f"HTTP error occurred: {http_err}"
        
        # Handle specific error codes
        if response.status_code == 401:
            error_message = "Unauthorized: Authentication token may have expired. Please update AUTH_TOKEN."
            try:
                error_details = response.json()
            except:
                error_details = response.text if response.text else "Token expired or invalid"
        elif response.status_code == 403:
            error_message = "Forbidden: API is blocking the request (likely Cloudflare protection). The API may be blocking requests from Vercel servers."
            try:
                error_details = response.json()
            except:
                # Check if it's a Cloudflare challenge page
                if "cloudflare" in response.text.lower() or "challenge" in response.text.lower():
                    error_details = "Cloudflare protection is blocking the request. This may require manual intervention or using a different hosting provider."
                else:
                    error_details = response.text[:500] if response.text else "Access forbidden"
        else:
            try:
                error_details = response.json()
            except:
                error_details = response.text if response.text else "No error details available"
        
        return jsonify({
            "developer": developer_info,
            "server_info": {
                **server_info,
                "status": "error",
                "error_code": response.status_code
            },
            "error": error_message,
            "status_code": response.status_code,
            "details": error_details
        }), response.status_code
        
    except requests.exceptions.RequestException as req_err:
        return jsonify({
            "developer": developer_info,
            "server_info": {
                **server_info,
                "status": "error"
            },
            "error": f"An error occurred: {req_err}"
        }), 500
        
    except json.JSONDecodeError:
        return jsonify({
            "developer": developer_info,
            "server_info": {
                **server_info,
                "status": "error"
            },
            "error": "Failed to decode JSON response.",
            "details": response.text
        }), 500

@app.route('/api/iusee', methods=['GET'])
def get_issue_info():
    """
    Fetches lottery issue information from draw API.
    Always uses current timestamp to get fresh data (fetches every time).
    Accepts ts (timestamp) as optional query parameter, but defaults to current time for fresh data.
    """
    # Always use current timestamp to fetch fresh data from API (updates every second)
    # This ensures start and end times are always current
    ts = str(int(time.time() * 1000))  # Current timestamp in milliseconds (always fresh)
    
    # Build URL with timestamp
    url = f"{DRAW_API_URL}?ts={ts}"
    
    # Headers as provided
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,bn-BD;q=0.8,bn;q=0.7",
        "origin": "https://bhtclub2.com",
        "priority": "u=1, i",
        "referer": "https://bhtclub2.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1"
    }
    
    # Developer info
    developer_info = {
        "name": "@nexcoder",
        "contact": "github.com/enzosrs"
    }
    
    # Server info
    server_info = {
        "timestamp": int(time.time()),
        "endpoint": "/api/iusee",
        "method": "GET",
        "status": "active"
    }
    
    try:
        # Use curl_cffi for Cloudflare bypass (best for serverless), fallback to cloudscraper, then requests
        if USE_CURL_CFFI:
            response = curl_requests.get(
                url, 
                headers=headers, 
                timeout=15, 
                allow_redirects=True,
                impersonate="chrome119"
            )
        elif USE_CLOUDSCRAPER:
            scraper = cloudscraper.create_scraper()
            scraper.headers.update(headers)
            response = scraper.get(url, timeout=15, allow_redirects=True)
        else:
            session = requests.Session()
            session.headers.update(headers)
            response = session.get(url, timeout=15, allow_redirects=True)
        response.raise_for_status()
        
        # Get API response data
        api_data = response.json()
        
        # Get server time from API response if available (for accurate calculation)
        # The API might return serviceTime or serverTime field
        api_server_time_ms = api_data.get("serviceTime") or api_data.get("serverTime") or api_data.get("currentTime")
        if not api_server_time_ms:
            # Fallback to our server time if API doesn't provide it
            api_server_time_ms = int(time.time() * 1000)
        
        # Convert timestamps to India/Asia/Kolkata timezone (IST = UTC+5:30)
        kolkata_offset = timedelta(hours=5, minutes=30)
        kolkata_tz = timezone(kolkata_offset)
        
        def convert_timestamp_to_time(ts_ms):
            """Convert milliseconds timestamp to HH:MM IST format"""
            if ts_ms:
                ts_seconds = ts_ms / 1000
                dt_utc = datetime.fromtimestamp(ts_seconds, tz=timezone.utc)
                dt_kolkata = dt_utc.astimezone(kolkata_tz)
                return dt_kolkata.strftime('%H:%M IST')
            return None
        
        def calculate_remaining_seconds(start_time_ms, end_time_ms, current_server_time_ms):
            """Calculate remaining seconds from current time to end time
            This should match exactly with the game's countdown (60 seconds, not 85)
            Uses the API's server time for accurate calculation"""
            if start_time_ms and end_time_ms:
                # Use the API's server time (not our local time) for accurate calculation
                # This ensures we match the game's countdown exactly
                current_time_ms = current_server_time_ms
                
                # The API timestamps (startTime, endTime) are absolute timestamps
                # Calculate remaining: end_time - current_server_time
                remaining_ms = end_time_ms - current_time_ms
                
                # Convert to seconds using floor division (matches game exactly)
                remaining_seconds = remaining_ms // 1000
                
                # Ensure non-negative
                if remaining_seconds < 0:
                    remaining_seconds = 0
                
                # The game shows the actual remaining time, so we should match it
                return remaining_seconds
            return 0
        
        # Build clean response matching the exact format
        clean_response = {
            "game": api_data.get("gameCode", "TrxWinGo_1M"),
            "timezone": "Asia/Kolkata",
            "success": True
        }
        
        # Process current round with live countdown (calculated from start and end times)
        if 'current' in api_data and api_data['current']:
            curr = api_data['current']
            start_time = curr.get("startTime", 0)
            end_time = curr.get("endTime", 0)
            
            # Convert start and end times to Asia/Kolkata timezone for display
            start_time_kolkata = convert_timestamp_to_time(start_time)
            end_time_kolkata = convert_timestamp_to_time(end_time)
            
            # Calculate remaining seconds using API's server time (to match game exactly)
            # This should show 60 seconds when game shows 60, not 85
            remaining_seconds = calculate_remaining_seconds(start_time, end_time, api_server_time_ms)
            
            clean_response['current_round'] = {
                "issue": curr.get("issueNumber", ""),
                "status": "active",
                "remaining": remaining_seconds,  # Remaining time in seconds (matches game exactly)
                "time": {
                    "start": start_time_kolkata,  # Converted to Asia/Kolkata timezone
                    "end": end_time_kolkata       # Converted to Asia/Kolkata timezone
                }
            }
        
        # Process next round
        if 'next' in api_data and api_data['next']:
            next_issue = api_data['next']
            clean_response['next_round'] = {
                "issue": next_issue.get("issueNumber", ""),
                "status": "upcoming",
                "time": {
                    "start": convert_timestamp_to_time(next_issue.get("startTime")),
                    "end": convert_timestamp_to_time(next_issue.get("endTime"))
                }
            }
        
        # Process previous round
        if 'previous' in api_data and api_data['previous']:
            prev = api_data['previous']
            clean_response['previous_round'] = {
                "issue": prev.get("issueNumber", ""),
                "status": "completed",
                "time": {
                    "start": convert_timestamp_to_time(prev.get("startTime")),
                    "end": convert_timestamp_to_time(prev.get("endTime"))
                }
            }
        
        # Add server info
        clean_response['server'] = {
            "endpoint": "/api/iusee",
            "method": "GET",
            "status": "active"
        }
        
        # Return clean response
        return jsonify(clean_response), 200
        
    except requests.exceptions.HTTPError as http_err:
        error_details = "No details available."
        try:
            error_details = response.json()
        except:
            error_details = response.text
        
        return jsonify({
            "developer": developer_info,
            "server_info": {
                **server_info,
                "status": "error",
                "error_code": response.status_code
            },
            "error": f"HTTP error occurred: {http_err}",
            "status_code": response.status_code,
            "details": error_details
        }), response.status_code
        
    except requests.exceptions.RequestException as req_err:
        return jsonify({
            "developer": developer_info,
            "server_info": {
                **server_info,
                "status": "error"
            },
            "error": f"An error occurred: {req_err}"
        }), 500
        
    except json.JSONDecodeError:
        return jsonify({
            "developer": developer_info,
            "server_info": {
                **server_info,
                "status": "error"
            },
            "error": "Failed to decode JSON response.",
            "details": response.text
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_trend_statistics():
    """
    Fetches lottery trend statistics from the external API.
    Accepts gameCode, pageNo, and pageSize as query parameters.
    """
    # Get Query Parameters
    game_code = request.args.get('gameCode', default="TrxWinGo_1M", type=str)
    page_no = request.args.get('pageNo', default=1, type=int)
    page_size = request.args.get('pageSize', default=10, type=int)
    
    # Use static payload format (as provided by user)
    params = {
        "gameCode": game_code,
        "pageNo": page_no,
        "pageSize": page_size,
        "language": "en",
        "random": "486136551970",
        "signature": "00518FED2F8F571D9451A13C4D313AB7",
        "timestamp": "1765720961"
    }
    
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,bn-BD;q=0.8,bn;q=0.7",
        "authorization": f"Bearer {AUTH_TOKEN}",
        "origin": "https://bhtclub2.com",
        "priority": "u=1, i",
        "referer": "https://bhtclub2.com/",
        "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "cache-control": "no-cache",
        "pragma": "no-cache"
    }
    
    # Developer info
    developer_info = {
        "name": "@nexcoder",
        "contact": "github.com/enzosrs"
    }
    
    # Server info
    server_info = {
        "timestamp": int(time.time()),
        "endpoint": "/api/stats",
        "method": "GET",
        "status": "active"
    }
    
    try:
        # Use curl_cffi for Cloudflare bypass (best for serverless), fallback to cloudscraper, then requests
        if USE_CURL_CFFI:
            response = curl_requests.get(
                STATS_API_URL, 
                params=params, 
                headers=headers, 
                timeout=15, 
                allow_redirects=True,
                impersonate="chrome119"
            )
        elif USE_CLOUDSCRAPER:
            scraper = cloudscraper.create_scraper()
            scraper.headers.update(headers)
            response = scraper.get(STATS_API_URL, params=params, timeout=15, allow_redirects=True)
        else:
            session = requests.Session()
            session.headers.update(headers)
            response = session.get(STATS_API_URL, params=params, timeout=15, allow_redirects=True)
        
        # Ensure response encoding is set correctly for proper text decoding
        if response.encoding is None or response.encoding == 'ISO-8859-1':
            response.encoding = 'utf-8'
        
        # Check if response is successful
        if response.status_code != 200:
            error_details = "No details available."
            error_message = f"HTTP error occurred: Status {response.status_code}"
            
            # Handle specific error codes
            if response.status_code == 401:
                error_message = "Unauthorized: Authentication token may have expired. Please update AUTH_TOKEN."
            elif response.status_code == 403:
                error_message = "Forbidden: API is blocking the request (likely Cloudflare protection). The API may be blocking requests from Vercel servers."
            
            try:
                # Try to get text (requests handles decompression automatically)
                response_text = response.text[:500] if response.text else None
                if response_text:
                    # Try to parse as JSON
                    try:
                        error_details = response.json()
                    except:
                        error_details = response_text
                else:
                    error_details = "Empty response from server"
            except Exception as e:
                error_details = f"Error reading response: {str(e)}"
            
            return jsonify({
                "developer": developer_info,
                "server_info": {
                    **server_info,
                    "status": "error",
                    "error_code": response.status_code
                },
                "error": error_message,
                "status_code": response.status_code,
                "details": error_details
            }), response.status_code
        
        # Check if response has content
        # Access response.text to trigger automatic decompression
        response_text = response.text if hasattr(response, 'text') else ""
        if not response_text or not response_text.strip():
            return jsonify({
                "developer": developer_info,
                "server_info": {
                    **server_info,
                    "status": "error"
                },
                "error": "Empty response from API",
                "status_code": response.status_code
            }), 500
        
        # Try to parse JSON response
        # Use response.json() which handles decompression automatically
        try:
            api_data = response.json()
        except json.JSONDecodeError as json_err:
            # If JSON decode fails, try to get the raw text for debugging
            try:
                preview = response.text[:500] if response.text else "Empty response"
            except:
                preview = "Could not read response text"
            
            return jsonify({
                "developer": developer_info,
                "server_info": {
                    **server_info,
                    "status": "error"
                },
                "error": f"Failed to decode JSON response: {str(json_err)}",
                "status_code": response.status_code,
                "response_content_type": response.headers.get("content-type", "unknown"),
                "content_encoding": response.headers.get("content-encoding", "none"),
                "response_preview": preview
            }), 500
        
        # Return response with developer and server info
        return jsonify({
            "developer": developer_info,
            "server_info": server_info,
            "data": api_data.get("data", []),
            "code": api_data.get("code", 0),
            "msg": api_data.get("msg", ""),
            "msgCode": api_data.get("msgCode", 0),
            "serviceTime": api_data.get("serviceTime")
        }), 200
        
    except requests.exceptions.HTTPError as http_err:
        error_details = "No details available."
        try:
            if 'response' in locals():
                error_details = response.json()
        except:
            if 'response' in locals():
                error_details = response.text[:500]
        
        return jsonify({
            "developer": developer_info,
            "server_info": {
                **server_info,
                "status": "error",
                "error_code": response.status_code if 'response' in locals() else None
            },
            "error": f"HTTP error occurred: {http_err}",
            "status_code": response.status_code if 'response' in locals() else None,
            "details": error_details
        }), response.status_code if 'response' in locals() else 500
        
    except requests.exceptions.RequestException as req_err:
        return jsonify({
            "developer": developer_info,
            "server_info": {
                **server_info,
                "status": "error"
            },
            "error": f"Request error occurred: {str(req_err)}",
            "error_type": type(req_err).__name__
        }), 500
        
    except Exception as e:
        return jsonify({
            "developer": developer_info,
            "server_info": {
                **server_info,
                "status": "error"
            },
            "error": f"Unexpected error: {str(e)}",
            "error_type": type(e).__name__
        }), 500

# Main execution block - Flask only
if __name__ == "__main__":
    print("=" * 60)
    print("Starting Lottery History API Server")
    print("=" * 60)
    print(f"API URL: {API_URL}")
    print(f"Draw API URL: {DRAW_API_URL}")
    print("\nAvailable endpoints:")
    print("  GET  /           - API Documentation (lists all endpoints)")
    print("  GET  /api/history - Fetch lottery history")
    print("  GET  /api/iusee   - Fetch lottery issue information with live countdown")
    print("  GET  /api/stats   - Fetch lottery trend statistics")
    print("\nExample usage:")
    print("  http://localhost:5000/")
    print("  http://localhost:5000/api/history?gameCode=TrxWinGo_1M&pageNo=1&pageSize=10")
    print("  http://localhost:5000/api/iusee?ts=1765719395722")
    print("  http://localhost:5000/api/iusee  (uses current timestamp)")
    print("  http://localhost:5000/api/stats?gameCode=TrxWinGo_1M&pageNo=1&pageSize=10")
    # For local development
    import os
    port = int(os.environ.get('PORT', 5000))
    print(f"\nStarting server on http://0.0.0.0:{port}")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    app.run(host='0.0.0.0', port=port, debug=False)
