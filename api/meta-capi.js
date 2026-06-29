const crypto = require('crypto');

// Standard SHA-256 hashing for GDPR/Meta compliance
function hashData(value) {
  if (!value) return null;
  const cleanValue = value.trim().toLowerCase();
  return crypto.createHash('sha256').update(cleanValue).digest('hex');
}

// Phone specific hashing (removes non-digits and leading zeros)
function hashPhone(value) {
  if (!value) return null;
  const cleanValue = value.replace(/\D/g, ''); // Keep only digits
  return crypto.createHash('sha256').update(cleanValue).digest('hex');
}

module.exports = async (req, res) => {
  // 1. Configure CORS Headers for security
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  // Handle OPTIONS request pre-flight
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method not allowed. Use POST.' });
    return;
  }

  // 2. Resolve Environment Variables
  const PIXEL_ID = process.env.META_PIXEL_ID || '1027355633035262';
  const CAPI_TOKEN = process.env.META_CAPI_TOKEN;
  const TEST_EVENT_CODE = process.env.META_TEST_EVENT_CODE;

  if (!CAPI_TOKEN) {
    console.error('Server Configuration Error: META_CAPI_TOKEN is missing.');
    res.status(500).json({ error: 'Server configuration error' });
    return;
  }

  try {
    const { eventName, eventId, eventID, eventSourceUrl, userData = {}, user_data = {}, customData = {} } = req.body;
    const resolvedEventId = eventId || eventID;

    if (!eventName || !resolvedEventId) {
      res.status(400).json({ error: 'Missing required parameters: eventName, eventId' });
      return;
    }

    // 3. Normalize and Hash User Data (Meta Matching Keys)
    const payloadUserData = {
      client_ip_address: req.headers['x-forwarded-for'] || req.socket.remoteAddress || null,
      client_user_agent: req.headers['user-agent'] || null,
    };

    // Support both client-side hashed (snake_case) and server-side unhashed (camelCase) user data
    if (user_data.em) {
      payloadUserData.em = Array.isArray(user_data.em) ? user_data.em : [user_data.em];
    } else if (userData.email) {
      payloadUserData.em = [hashData(userData.email)];
    }

    if (user_data.ph) {
      payloadUserData.ph = Array.isArray(user_data.ph) ? user_data.ph : [user_data.ph];
    } else if (userData.phone) {
      payloadUserData.ph = [hashPhone(userData.phone)];
    }

    if (user_data.fn) {
      payloadUserData.fn = Array.isArray(user_data.fn) ? user_data.fn : [user_data.fn];
    } else if (userData.name) {
      payloadUserData.fn = [hashData(userData.name)];
    }

    // 4. Construct Meta CAPI Payload
    const capiEvent = {
      event_name: eventName,
      event_time: Math.floor(Date.now() / 1000),
      event_id: eventId,
      event_source_url: eventSourceUrl || req.headers.referer || 'https://www.fdlsorterai.com/',
      action_source: 'website',
      user_data: payloadUserData,
      custom_data: customData,
      opt_out: false
    };

    const postBody = {
      data: [capiEvent]
    };

    // Attach Test Event Code if provided in environment
    if (TEST_EVENT_CODE) {
      postBody.test_event_code = TEST_EVENT_CODE;
    }

    // 5. Fire Request to Meta Graph API
    const metaResponse = await fetch(
      `https://graph.facebook.com/v19.0/${PIXEL_ID}/events?access_token=${CAPI_TOKEN}`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(postBody)
      }
    );

    const result = await metaResponse.json();
    res.status(metaResponse.status).json(result);

  } catch (error) {
    console.error('Meta CAPI Proxy Exception:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
};
