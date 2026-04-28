export default async function handler(req, res) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');

  // Handle preflight
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, error: 'Method not allowed' });
  }

  try {
    const data = req.body;
    
    // Validation
    const { name, email, phone, address, telegram, payment_method, delivery_method, items } = data;
    
    if (!name || !email || !phone || !address || !telegram || !payment_method || !delivery_method) {
      return res.status(400).json({ success: false, error: 'Все обязательные поля должны быть заполнены' });
    }

    if (!items || items.length === 0) {
      return res.status(400).json({ success: false, error: 'Корзина пуста' });
    }

    // Generate order ID
    const order_id = `ORD-${Date.now()}`;

    // Calculate total
    const total_amount = items.reduce((sum, item) => sum + (item.price * item.quantity), 0);

    // Format Telegram message
    let message = `🛍 *Новый заказ ${order_id}*\n\n`;
    message += `👤 *Покупатель:*\n`;
    message += `Имя: ${name}\n`;
    message += `Email: ${email}\n`;
    message += `Телефон: ${phone}\n`;
    message += `Telegram: ${telegram}\n`;
    message += `Адрес: ${address}\n\n`;
    
    message += `📦 *Товары:*\n`;
    items.forEach((item, index) => {
      message += `${index + 1}. ${item.product_name}\n`;
      message += `   Размер: ${item.size}\n`;
      message += `   Количество: ${item.quantity}\n`;
      message += `   Цена: ${item.price} ₽\n\n`;
    });
    
    message += `💳 *Способ оплаты:* ${payment_method === 'card' ? 'Карта' : 'Крипта'}\n`;
    message += `🚚 *Доставка:* ${delivery_method === 'cdek' ? 'СДЕК' : 'Ozon'}\n\n`;
    message += `💰 *Итого: ${total_amount} ₽*`;

    // Send to Telegram
    const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN || '8636156376:AAHOTTH-dxOiRDMZsC8FqrG_fBQgcnFPiYU';
    const TELEGRAM_CHAT_ID = process.env.TELEGRAM_CHAT_ID || '6738586683';
    
    const telegramUrl = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;
    
    const telegramResponse = await fetch(telegramUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: TELEGRAM_CHAT_ID,
        text: message,
        parse_mode: 'Markdown'
      })
    });

    if (!telegramResponse.ok) {
      console.error('Telegram API error:', await telegramResponse.text());
      return res.status(500).json({ success: false, error: 'Не удалось отправить заказ. Попробуйте позже.' });
    }

    return res.status(200).json({
      success: true,
      order_id,
      total_amount
    });

  } catch (error) {
    console.error('Checkout error:', error);
    return res.status(500).json({ success: false, error: 'Произошла ошибка при обработке заказа' });
  }
}
