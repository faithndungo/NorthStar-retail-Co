export default function Home({ onNavigate }) {
  const services = [
    {
      key: 'order',
      icon: '01',
      title: 'Track your order',
      description: 'See live progress, delivery timing, and package details.',
      action: 'Track an order'
    },
    {
      key: 'return',
      icon: '02',
      title: 'Start a return',
      description: 'Check eligibility and create a return in a few guided steps.',
      action: 'Begin a return'
    },
    {
      key: 'stock',
      icon: '03',
      title: 'Check availability',
      description: 'Find the right size and color or request a restock alert.',
      action: 'Check stock'
    }
  ];

  return (
    <div className="home-page">
      <section className="home-hero">
        <div className="hero-copy">
          <span className="eyebrow">Customer care, simplified</span>
          <h1>Answers at your fingertips.</h1>
          <p>
            Track a delivery, arrange a return, or find an item in stock—without
            waiting for a support agent.
          </p>
          <button type="button" onClick={() => onNavigate('order')}>
            Track my order <span aria-hidden="true">→</span>
          </button>
        </div>
        <div className="hero-orbit" aria-hidden="true">
          <span className="orbit-ring" />
          <span className="orbit-core">N</span>
          <span className="orbit-label orbit-label-one">Fast</span>
          <span className="orbit-label orbit-label-two">Simple</span>
          <span className="orbit-label orbit-label-three">24/7</span>
        </div>
      </section>

      <section className="service-section" aria-labelledby="service-heading">
        <div className="section-heading">
          <div>
            <span className="eyebrow">Self-service</span>
            <h2 id="service-heading">How can we help?</h2>
          </div>
          <p>Choose a task and we’ll guide you through it.</p>
        </div>

        <div className="service-grid">
          {services.map((service) => (
            <button
              key={service.key}
              type="button"
              className="service-card"
              onClick={() => onNavigate(service.key)}
            >
              <span className="service-number">{service.icon}</span>
              <span className="service-title">{service.title}</span>
              <span className="service-description">{service.description}</span>
              <span className="service-link">{service.action} →</span>
            </button>
          ))}
        </div>
      </section>

      <section className="trust-strip" aria-label="NorthStar service benefits">
        <div><strong>24/7</strong><span>Self-service access</span></div>
        <div><strong>Live</strong><span>Order and stock data</span></div>
        <div><strong>Secure</strong><span>Verified order lookup</span></div>
        <div><strong>Simple</strong><span>Guided return process</span></div>
      </section>
    </div>
  );
}
