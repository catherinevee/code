import React, { useState, useEffect } from 'react';

// Data for dormitories
const dormitoriesData = [
  {
    id: 'alpha-hall',
    name: 'Alpha Hall',
    image: 'https://placehold.co/600x400/D8BFD8/000000?text=Alpha+Hall', // Mauve placeholder
    description: 'Traditional style dorms with shared bathrooms, perfect for first-year students seeking a classic college experience.',
    features: [
      'Double and Triple Rooms',
      'Spacious Community Lounges',
      'Dedicated Study Areas',
      'High-speed Wi-Fi',
      'On-site Laundry',
      '24/7 Security'
    ],
    fullDescription: 'Alpha Hall offers a vibrant and classic dormitory experience, ideal for new students. Located centrally on campus, it provides easy access to academic buildings and dining halls. Residents enjoy shared living spaces, fostering strong community bonds through various social events and study groups organized by resident advisors. Each floor has common bathrooms and comfortable lounges equipped with seating and study tables. The building is equipped with modern amenities including high-speed internet, secure entry systems, and convenient laundry facilities on every floor. Our dedicated staff ensures a safe and welcoming environment for all residents.'
  },
  {
    id: 'beta-residence',
    name: 'Beta Residence',
    image: 'https://placehold.co/600x400/E6E6FA/000000?text=Beta+Residence', // Mauve placeholder
    description: 'Suite-style living with private bedrooms and shared common areas, offering more independence.',
    features: [
      'Single and Double Rooms',
      'Private Bathrooms (shared by suite)',
      'Convenient Kitchenettes',
      'Quiet Study Floors',
      'Fitness Room Access',
      'Resident Parking'
    ],
    fullDescription: 'Beta Residence provides a more independent living experience with its suite-style accommodations. Each suite consists of multiple private bedrooms sharing a common living area and a private bathroom. This setup is popular among upper-classmen and transfer students who appreciate a balance of privacy and community. Many suites include a kitchenette for light meal preparation, adding to the convenience. The building boasts quiet study floors, a communal fitness room, and ample resident parking. Security is a top priority, with controlled access and on-site staff available around the clock.'
  },
  {
    id: 'gamma-commons',
    name: 'Gamma Commons',
    image: 'https://placehold.co/600x400/DDA0DD/000000?text=Gamma+Commons', // Mauve placeholder
    description: 'Apartment-style units with full kitchens and living rooms, ideal for upper-year students.',
    features: [
      'Private Single Bedrooms',
      'Modern Full Kitchens',
      'On-site Laundry Facilities',
      'Individual Climate Control',
      'Furnished Options Available',
      'Pet-Friendly (select units)'
    ],
    fullDescription: 'Gamma Commons offers spacious apartment-style living, perfect for students seeking maximum independence and comfort. Each unit features private single bedrooms, a full kitchen with appliances, and a comfortable living room. This arrangement allows students to cook their own meals and host friends in a home-like setting. The building includes on-site laundry facilities, individual climate control in each apartment, and options for furnished units. Some units are even pet-friendly, allowing students to bring their beloved companions. Gamma Commons is designed for mature students who desire a quieter, more self-sufficient living environment.'
  },
  {
    id: 'delta-lodge',
    name: 'Delta Lodge',
    image: 'https://placehold.co/600x400/F0F8FF/000000?text=Delta+Lodge', // Mauve placeholder
    description: 'Cozy, traditional dorms with a focus on community building and social events.',
    features: [
      'Shared Double Rooms',
      'Large Common Area',
      'Game Room',
      'Outdoor Patio',
      'Resident-led Activities',
      'Close to Dining Hall'
    ],
    fullDescription: 'Delta Lodge is known for its strong sense of community and frequent social gatherings. It offers traditional shared double rooms, making it a great choice for students who want to connect with their peers. The lodge features a spacious common area, a dedicated game room, and an inviting outdoor patio perfect for relaxation and events. Resident advisors actively organize various activities, from movie nights to study groups, ensuring a lively and supportive atmosphere. Its proximity to the main dining hall adds to the convenience for residents.'
  },
  {
    id: 'epsilon-apartments',
    name: 'Epsilon Apartments',
    image: 'https://placehold.co/600x400/F5F5DC/000000?text=Epsilon+Apartments', // Mauve placeholder
    description: 'Modern apartment-style living with private bedrooms and shared living spaces, ideal for groups.',
    features: [
      '2-bedroom Apartments',
      'Full Kitchens',
      'Spacious Living Rooms',
      'In-unit Laundry',
      'Private Balconies',
      'Study Nooks'
    ],
    fullDescription: 'Epsilon Apartments provide a premium living experience with modern, fully-equipped 2-bedroom units. Each apartment includes a full kitchen, a spacious living room, and convenient in-unit laundry facilities. This option is perfect for students who prefer to live with a roommate or a small group, offering both privacy and shared common areas. Many units feature private balconies with campus views, and dedicated study nooks are integrated into the design for academic focus. The building offers contemporary finishes and a comfortable, independent living environment.'
  },
  {
    id: 'zeta-suites',
    name: 'Zeta Suites',
    image: 'https://placehold.co/600x400/FFF0F5/000000?text=Zeta+Suites', // Mauve placeholder
    description: 'Upscale suite-style dorms with enhanced amenities and a focus on academic support.',
    features: [
      'Single Occupancy Rooms',
      'En-suite Bathrooms',
      'Shared Study Lounges',
      'Academic Mentoring Program',
      'Soundproofed Walls',
      'Premium Furnishings'
    ],
    fullDescription: 'Zeta Suites offers an upscale living experience designed to support academic success. Each suite features single occupancy rooms with private en-suite bathrooms, providing maximum privacy and comfort. The building includes multiple shared study lounges, equipped with whiteboards and group tables, perfect for collaborative learning. Residents benefit from an exclusive academic mentoring program and quiet hours are strictly enforced. The rooms are soundproofed to minimize distractions, and all units come with premium furnishings, ensuring a comfortable and conducive environment for studying and relaxation.'
  },
  {
    id: 'eta-residence',
    name: 'Eta Residence',
    image: 'https://placehold.co/600x400/F8F8FF/000000?text=Eta+Residence', // Mauve placeholder
    description: 'Eco-friendly dorms with sustainable features and a focus on healthy living.',
    features: [
      'Recycled Material Furnishings',
      'Energy-efficient Appliances',
      'Community Garden Access',
      'Bike Storage',
      'Wellness Programs',
      'Composting Facilities'
    ],
    fullDescription: 'Eta Residence is our commitment to sustainable living, offering eco-friendly dorms with a range of green features. The building is constructed with recycled materials and furnished with sustainable pieces. Residents benefit from energy-efficient appliances and access to a vibrant community garden. Extensive bike storage encourages eco-conscious transportation, and the residence hosts various wellness programs, including yoga and meditation sessions. On-site composting facilities promote responsible waste management, making Eta Residence ideal for environmentally-minded students.'
  },
  {
    id: 'theta-hall',
    name: 'Theta Hall',
    image: 'https://placehold.co/600x400/F0FFF0/000000?text=Theta+Hall', // Mauve placeholder
    description: 'Large, lively dorm known for its diverse community and wide range of student organizations.',
    features: [
      'Mixed Gender Floors',
      'Large Recreation Room',
      'Cafeteria On-site',
      'Multicultural Events',
      'Student Organization Hub',
      '24-hour Front Desk'
    ],
    fullDescription: 'Theta Hall is the largest and most diverse dormitory on campus, a hub of activity and student life. It features mixed-gender floors and a massive recreation room equipped for various games and social gatherings. A convenient on-site cafeteria serves a variety of meal options. Theta Hall is renowned for its multicultural events and serves as a central hub for many student organizations, offering countless opportunities to get involved. A 24-hour front desk provides continuous support and security for all residents.'
  }
];

// Component for displaying a single dormitory's detailed page
const DormDetailPage = ({ dorm, onBack }) => (
  <section className="bg-white p-10 rounded-3xl shadow-2xl border border-purple-200 animate-fade-in">
    <button
      onClick={onBack}
      className="mb-8 px-6 py-2 bg-purple-600 text-white rounded-full font-semibold text-lg hover:bg-purple-700 transition-colors duration-300 shadow-md flex items-center"
    >
      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
        <path strokeLinecap="round" strokeLinejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
      </svg>
      Back to Dorms
    </button>
    <h2 className="text-5xl font-extrabold text-purple-800 mb-8 text-center leading-tight">{dorm.name}</h2>
    <div className="flex flex-col md:flex-row gap-8 items-start">
      <img
        src={dorm.image}
        alt={dorm.name}
        className="w-full md:w-1/2 rounded-2xl shadow-xl object-cover h-80 md:h-auto"
        onError={(e) => { e.target.onerror = null; e.target.src = "https://placehold.co/600x400/CCCCCC/000000?text=Image+Not+Found"; }}
      />
      <div className="md:w-1/2">
        <p className="text-xl text-gray-700 mb-6 leading-relaxed">{dorm.fullDescription}</p>
        <h3 className="text-3xl font-bold text-purple-700 mb-4">Key Features:</h3>
        <ul className="list-disc list-inside text-gray-700 mb-6 text-lg space-y-2">
          {dorm.features.map((feature, index) => (
            <li key={index}>{feature}</li>
          ))}
        </ul>
        <button className="w-full bg-purple-600 text-white py-4 rounded-xl font-bold text-2xl hover:bg-purple-700 transition-colors duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
          Apply for {dorm.name}
        </button>
      </div>
    </div>
  </section>
);

// FAQ Content as a separate component for cleaner rendering
const FAQPage = () => (
  <section className="bg-white p-10 rounded-3xl shadow-2xl border border-purple-200 animate-fade-in">
    <h2 className="text-5xl font-extrabold text-purple-800 mb-8 text-center leading-tight">First-Time Dorm Mover FAQ</h2>
    <p className="text-xl text-gray-700 mb-10 text-center max-w-4xl mx-auto">
      Moving into a college dorm for the first time can bring up a lot of questions! Here are some common inquiries from new students to help you prepare for your arrival at Evergreen University.
    </p>

    <div className="space-y-8">
      {/* FAQ Item 1 */}
      <div>
        <h3 className="text-3xl font-bold text-purple-700 mb-2">Q1: What are the official move-in dates and times?</h3>
        <p className="text-lg text-gray-700 leading-relaxed">
          **A1:** Official move-in for Fall 2025 is **August 20th, from 9:00 AM to 5:00 PM**. Early arrival is by request only for specific groups (e.g., athletes, orientation leaders) and is scheduled for August 18th-19th. Please check your housing portal for your assigned move-in window to help manage traffic flow.
        </p>
      </div>

      {/* FAQ Item 2 */}
      <div>
        <h3 className="text-3xl font-bold text-purple-700 mb-2">Q2: What should I pack, and what should I leave at home?</h3>
        <p className="text-lg text-gray-700 leading-relaxed">
          **A2:** We recommend packing light! Essentials include bedding (XL Twin size), toiletries, towels, school supplies, a desk lamp, and clothes. Don't forget a power strip with surge protection. Leave large furniture, excessive electronics, candles, hot plates, and anything that violates fire safety regulations at home. A detailed checklist is available on the "Moving In" page of our housing website.
        </p>
      </div>

      {/* FAQ Item 3 */}
      <div>
        <h3 className="text-3xl font-bold text-purple-700 mb-2">Q3: Can I bring my own mini-fridge or microwave?</h3>
        <p className="text-lg text-gray-700 leading-relaxed">
          **A3:** Mini-fridges are generally allowed, but they must be under a certain size and wattage (typically 4.5 cubic feet or less, and energy-star rated). Microwaves are usually only permitted in designated common areas or in apartment-style dorms with full kitchens (like Gamma Commons or Epsilon Apartments). Please check your specific dorm's guidelines for exact rules.
        </p>
      </div>

      {/* FAQ Item 4 */}
      <div>
        <h3 className="text-3xl font-bold text-purple-700 mb-2">Q4: How do I get my belongings to my room, and will there be help?</h3>
        <p className="text-lg text-gray-700 leading-relaxed">
          **A4:** On official move-in day, there will be student volunteers and staff available to assist with unloading vehicles and transporting belongings to your room. We recommend labeling all your boxes with your name and dorm room number. Dollies and carts will also be available for use.
        </p>
      </div>

      {/* FAQ Item 5 */}
      <div>
        <h3 className="text-3xl font-bold text-purple-700 mb-2">Q5: What kind of internet access is available in the dorms?</h3>
        <p className="text-lg text-gray-700 leading-relaxed">
          **A5:** All dorm rooms are equipped with high-speed Wi-Fi access. Ethernet ports are also available in each room if you prefer a wired connection. Information on connecting your devices will be provided upon check-in.
        </p>
      </div>

      {/* FAQ Item 6 */}
      <div>
        <h3 className="text-3xl font-bold text-purple-700 mb-2">Q6: Can I decorate my room? Are there any restrictions?</h3>
        <p className="text-lg text-gray-700 leading-relaxed">
          **A6:** Yes, we encourage you to personalize your space! However, there are some restrictions for safety and to prevent damage. Avoid using nails, screws, or anything that will permanently damage walls. Command strips, poster putty, and removable adhesive hooks are generally safe options. Open flames (candles, incense), excessive string lights, and anything that obstructs fire alarms or sprinklers are strictly prohibited.
        </p>
      </div>

      {/* FAQ Item 7 */}
      <div>
        <h3 className="text-3xl font-bold text-purple-700 mb-2">Q7: What are the rules about guests in the dorms?</h3>
        <p className="text-lg text-gray-700 leading-relaxed">
          **A7:** Guests are generally permitted during specific hours, but policies vary by dorm and university regulations. Overnight guests may require prior registration and approval from your Resident Advisor (RA) and roommate(s). All guests must abide by university policies and be accompanied by their host resident at all times.
        </p>
      </div>

      {/* FAQ Item 8 */}
      <div>
        <h3 className="text-3xl font-bold text-purple-700 mb-2">Q8: What if I have a conflict with my roommate?</h3>
        <p className="text-lg text-gray-700 leading-relaxed">
          **A8:** Our Resident Advisors (RAs) are trained to help facilitate positive roommate relationships. If conflicts arise, your RA is your first point of contact. They can help mediate discussions and find solutions. Open communication is key!
        </p>
      </div>

      {/* FAQ Item 9 */}
      <div>
        <h3 className="text-3xl font-bold text-purple-700 mb-2">Q9: Is there laundry available in the dorms?</h3>
        <p className="text-lg text-gray-700 leading-relaxed">
          **A9:** Yes, all dormitories have communal laundry facilities, typically located on each floor or in the basement. These facilities are equipped with washers and dryers. Some dorms may use a card-based system or a mobile app for payment.
        </p>
      </div>

      {/* FAQ Item 10 */}
      <div>
        <h3 className="text-3xl font-bold text-purple-700 mb-2">Q10: What kind of security measures are in place in the dorms?</h3>
        <p className="text-lg text-gray-700 leading-relaxed">
          **A10:** Student safety is a top priority. All dorms have controlled access systems (card swipe entry), and many have 24/7 front desk staff. Security cameras are installed in common areas, and Resident Advisors are on duty. We encourage all students to report any suspicious activity immediately.
        </p>
      </div>
    </div>
  </section>
);

// About Us Page Component
const AboutUsPage = () => (
  <section className="bg-white p-10 rounded-3xl shadow-2xl border border-purple-200 animate-fade-in">
    <h2 className="text-5xl font-extrabold text-purple-800 mb-8 text-center leading-tight">About Evergreen University</h2>
    <p className="text-xl text-gray-700 mb-10 text-center max-w-4xl mx-auto">
      Evergreen University is dedicated to providing a cutting-edge learning environment, and at the heart of this commitment are our advanced technology infrastructures. We believe that seamless and rapid connectivity is fundamental to modern education and student life.
    </p>

    <div className="flex flex-col md:flex-row gap-8 items-start mb-12">
      <img
        src="https://placehold.co/600x400/ADD8E6/000000?text=Network+Infrastructure"
        alt="Network Infrastructure"
        className="w-full md:w-1/2 rounded-2xl shadow-xl object-cover h-80 md:h-auto"
        onError={(e) => { e.target.onerror = null; e.target.src = "https://placehold.co/600x400/CCCCCC/000000?text=Image+Not+Found"; }}
      />
      <div className="md:w-1/2">
        <h3 className="text-3xl font-bold text-purple-700 mb-4">Ultra-Fast Campus Internet</h3>
        <p className="text-lg text-gray-700 mb-6 leading-relaxed">
          Our campus boasts a robust fiber-optic backbone, delivering gigabit-speed internet directly to dorm rooms, academic buildings, and common areas. This ensures that students and faculty have access to the bandwidth they need for research, online learning, streaming, and collaboration without interruption. We continuously monitor and upgrade our network to stay ahead of technological demands.
        </p>
        <ul className="list-disc list-inside text-gray-700 text-lg space-y-2">
          <li>Dedicated Fiber-Optic Network</li>
          <li>Gigabit Speeds for All Users</li>
          <li>Redundant Connections for Reliability</li>
          <li>24/7 Network Monitoring</li>
        </ul>
      </div>
    </div>

    <div className="flex flex-col md:flex-row-reverse gap-8 items-start">
      <img
        src="https://placehold.co/600x400/DDA0DD/000000?text=Wireless+Network"
        alt="Wireless Network"
        className="w-full md:w-1/2 rounded-2xl shadow-xl object-cover h-80 md:h-auto"
        onError={(e) => { e.target.onerror = null; e.target.src = "https://placehold.co/600x400/CCCCCC/000000?text=Image+Not+Found"; }}
      />
      <div className="md:w-1/2">
        <h3 className="text-3xl font-bold text-purple-700 mb-4">Seamless Campus-Wide Wireless Coverage</h3>
        <p className="text-lg text-gray-700 mb-6 leading-relaxed">
          From the lecture halls to the green spaces, Evergreen University provides pervasive and high-performance wireless connectivity. Our Wi-Fi 6 (802.11ax) network ensures low latency and high capacity, supporting a multitude of devices simultaneously. Students can move freely across campus without losing connection, making it easy to stay productive anywhere.
        </p>
        <ul className="list-disc list-inside text-gray-700 text-lg space-y-2">
          <li>Latest Wi-Fi 6 (802.11ax) Technology</li>
          <li>High-Density Access Points</li>
          <li>Secure & Encrypted Connections</li>
          <li>Guest Network Availability</li>
        </ul>
      </div>
    </div>

    <div className="mt-16 text-center">
      <h3 className="text-4xl font-bold text-purple-800 mb-6">Our Commitment to Innovation</h3>
      <p className="text-xl text-gray-700 max-w-4xl mx-auto">
        Evergreen University continually invests in emerging technologies to enhance the student experience. Our IT department works tirelessly to implement the latest advancements in network security, cloud computing, and smart campus initiatives, ensuring that our students are always at the forefront of technological progress.
      </p>
    </div>
  </section>
);


// Main App component
const App = () => {
  // State to manage the active tab/section (dorms, off-campus, resources, tech-support, dining-hall, moving-in, faq, on-campus-jobs, about-us)
  const [activeTab, setActiveTab] = useState('dorms');
  // State to manage which dormitory detail page is currently displayed
  // null means no specific dorm page is active, showing the list
  const [selectedDorm, setSelectedDorm] = useState(null);
  // State to manage a simple form submission message for general inquiry
  const [formMessage, setFormMessage] = useState('');
  // State to manage a simple form submission message for tech support
  const [techSupportMessage, setTechSupportMessage] = useState('');


  // Effect to clear general inquiry form message after a few seconds
  useEffect(() => {
    if (formMessage) {
      const timer = setTimeout(() => {
        setFormMessage('');
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [formMessage]);

  // Effect to clear tech support form message after a few seconds
  useEffect(() => {
    if (techSupportMessage) {
      const timer = setTimeout(() => {
        setTechSupportMessage('');
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [techSupportMessage]);

  // Function to handle general inquiry form submission (client-side only)
  const handleSubmitInquiry = (e) => {
    e.preventDefault();
    // In a real application, this would send data to a Node.js backend
    setFormMessage('Your inquiry has been submitted! We will get back to you soon.');
    e.target.reset(); // Clear the form
  };

  // Function to handle tech support form submission (client-side only)
  const handleSubmitTechSupport = (e) => {
    e.preventDefault();
    // In a real application, this would send data to a Node.js backend
    setTechSupportMessage('Your technical support request has been submitted. A technician will contact you shortly!');
    e.target.reset(); // Clear the form
  };

  // Function to navigate to a specific dorm's detail page
  const handleViewDormDetails = (dormId) => {
    const dorm = dormitoriesData.find(d => d.id === dormId);
    setSelectedDorm(dorm);
    setActiveTab('dorms'); // Keep dorms tab active when viewing a dorm detail
  };

  // Function to go back to the main dormitories list
  const handleBackToDorms = () => {
    setSelectedDorm(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-fuchsia-100 font-inter text-gray-800">
      {/* Header Section */}
      <header className="bg-gradient-to-r from-fuchsia-700 to-purple-600 shadow-lg py-5 px-6 md:px-12 flex flex-col rounded-b-3xl">
        <div className="flex flex-col md:flex-row justify-between items-center mb-4">
          <div className="flex items-center mb-4 md:mb-0">
            <img src="https://placehold.co/60x60/FFFFFF/000000?text=EU" alt="University Logo" className="h-16 w-16 mr-4 rounded-full shadow-md" />
            <h1 className="text-4xl font-extrabold text-white drop-shadow-md">
              <span className="text-fuchsia-200">Evergreen</span> University
            </h1>
          </div>
          <div className="flex items-center space-x-4">
            <div className="relative">
              <input
                type="text"
                placeholder="Search..."
                className="pl-10 pr-4 py-2 rounded-full bg-white bg-opacity-20 text-white placeholder-fuchsia-100 focus:outline-none focus:ring-2 focus:ring-white focus:bg-opacity-30 transition-all duration-300 text-lg"
              />
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-fuchsia-100 absolute left-3 top-1/2 transform -translate-y-1/2" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <button className="px-6 py-2 bg-white text-fuchsia-700 rounded-full font-bold text-lg hover:bg-fuchsia-100 transition-colors duration-300 shadow-md">
              Apply Now
            </button>
          </div>
        </div>

        <nav className="flex flex-wrap justify-center gap-6 mt-4 md:mt-0"> {/* Increased gap for better separation */}

          {/* Housing Group */}
          <div className="bg-fuchsia-800/10 p-3 rounded-xl flex flex-wrap justify-center gap-3 shadow-inner">
            <span className="text-fuchsia-100 font-bold text-sm uppercase mb-2 w-full text-center">Housing</span>
            <button
              onClick={() => { setActiveTab('dorms'); setSelectedDorm(null); }}
              className={`px-5 py-2 rounded-full font-semibold text-lg transition-all duration-300 ease-in-out transform hover:scale-105
                ${activeTab === 'dorms' ? 'bg-gradient-to-r from-white to-fuchsia-100 text-fuchsia-700 shadow-xl' : 'text-fuchsia-100 hover:bg-fuchsia-800 hover:text-white hover:shadow-md'}`}
            >
              Dormitories
            </button>
            <button
              onClick={() => { setActiveTab('off-campus'); setSelectedDorm(null); }}
              className={`px-5 py-2 rounded-full font-semibold text-lg transition-all duration-300 ease-in-out transform hover:scale-105
                ${activeTab === 'off-campus' ? 'bg-gradient-to-r from-white to-fuchsia-100 text-fuchsia-700 shadow-xl' : 'text-fuchsia-100 hover:bg-fuchsia-800 hover:text-white hover:shadow-md'}`}
            >
              Off-Campus
            </button>
            <button
              onClick={() => { setActiveTab('moving-in'); setSelectedDorm(null); }}
              className={`px-5 py-2 rounded-full font-semibold text-lg transition-all duration-300 ease-in-out transform hover:scale-105
                ${activeTab === 'moving-in' ? 'bg-gradient-to-r from-white to-fuchsia-100 text-fuchsia-700 shadow-xl' : 'text-fuchsia-100 hover:bg-fuchsia-800 hover:text-white hover:shadow-md'}`}
            >
              Moving In
            </button>
          </div>

          {/* Student Services Group */}
          <div className="bg-fuchsia-800/10 p-3 rounded-xl flex flex-wrap justify-center gap-3 shadow-inner">
            <span className="text-fuchsia-100 font-bold text-sm uppercase mb-2 w-full text-center">Student Services</span>
            <button
              onClick={() => { setActiveTab('resources'); setSelectedDorm(null); }}
              className={`px-5 py-2 rounded-full font-semibold text-lg transition-all duration-300 ease-in-out transform hover:scale-105
                ${activeTab === 'resources' ? 'bg-gradient-to-r from-white to-fuchsia-100 text-fuchsia-700 shadow-xl' : 'text-fuchsia-100 hover:bg-fuchsia-800 hover:text-white hover:shadow-md'}`}
            >
              Resources
            </button>
            <button
              onClick={() => { setActiveTab('tech-support'); setSelectedDorm(null); }}
              className={`px-5 py-2 rounded-full font-semibold text-lg transition-all duration-300 ease-in-out transform hover:scale-105
                ${activeTab === 'tech-support' ? 'bg-gradient-to-r from-white to-fuchsia-100 text-fuchsia-700 shadow-xl' : 'text-fuchsia-100 hover:bg-fuchsia-800 hover:text-white hover:shadow-md'}`}
            >
              Tech Support
            </button>
            <button
              onClick={() => { setActiveTab('dining-hall'); setSelectedDorm(null); }}
              className={`px-5 py-2 rounded-full font-semibold text-lg transition-all duration-300 ease-in-out transform hover:scale-105
                ${activeTab === 'dining-hall' ? 'bg-gradient-to-r from-white to-fuchsia-100 text-fuchsia-700 shadow-xl' : 'text-fuchsia-100 hover:bg-fuchsia-800 hover:text-white hover:shadow-md'}`}
            >
              Dining Hall
            </button>
            <button
              onClick={() => { setActiveTab('faq'); setSelectedDorm(null); }}
              className={`px-5 py-2 rounded-full font-semibold text-lg transition-all duration-300 ease-in-out transform hover:scale-105
                ${activeTab === 'faq' ? 'bg-gradient-to-r from-white to-fuchsia-100 text-fuchsia-700 shadow-xl' : 'text-fuchsia-100 hover:bg-fuchsia-800 hover:text-white hover:shadow-md'}`}
            >
              FAQ
            </button>
            <button
              onClick={() => { setActiveTab('on-campus-jobs'); setSelectedDorm(null); }}
              className={`px-5 py-2 rounded-full font-semibold text-lg transition-all duration-300 ease-in-out transform hover:scale-105
                ${activeTab === 'on-campus-jobs' ? 'bg-gradient-to-r from-white to-fuchsia-100 text-fuchsia-700 shadow-xl' : 'text-fuchsia-100 hover:bg-fuchsia-800 hover:text-white hover:shadow-md'}`}
            >
              On-Campus Jobs
            </button>
            <button
              onClick={() => { setActiveTab('about-us'); setSelectedDorm(null); }}
              className={`px-5 py-2 rounded-full font-semibold text-lg transition-all duration-300 ease-in-out transform hover:scale-105
                ${activeTab === 'about-us' ? 'bg-gradient-to-r from-white to-fuchsia-100 text-fuchsia-700 shadow-xl' : 'text-fuchsia-100 hover:bg-fuchsia-800 hover:text-white hover:shadow-md'}`}
            >
              About Us
            </button>
          </div>
        </nav>
      </header>

      {/* Main Content Area */}
      <main className="container mx-auto p-8 md:p-12">
        {/* Conditional rendering based on activeTab and selectedDorm */}
        {activeTab === 'dorms' && (
          selectedDorm ? (
            <DormDetailPage dorm={selectedDorm} onBack={handleBackToDorms} />
          ) : (
            <>
              {/* Hero Section for Homepage */}
              <section className="relative bg-gradient-to-br from-purple-700 to-fuchsia-800 rounded-3xl shadow-2xl overflow-hidden mb-12 h-96 flex items-center justify-center text-white p-8">
                <img
                  src="https://placehold.co/1200x500/5B21B6/FFFFFF?text=Welcome+to+Evergreen+University"
                  alt="Campus Hero"
                  className="absolute inset-0 w-full h-full object-cover opacity-30"
                />
                <div className="relative z-10 text-center">
                  <h2 className="text-6xl font-extrabold mb-4 drop-shadow-lg leading-tight">
                    Your Future Starts Here
                  </h2>
                  <p className="text-2xl mb-8 max-w-2xl mx-auto opacity-90">
                    Discover a world of opportunities, innovation, and community at Evergreen University.
                  </p>
                  <button className="px-8 py-4 bg-white text-purple-800 rounded-full font-bold text-xl shadow-lg hover:bg-fuchsia-100 transition-colors duration-300 transform hover:-translate-y-1">
                    Explore Programs
                  </button>
                </div>
              </section>

              <section className="bg-white p-10 rounded-3xl shadow-2xl border border-purple-200 animate-fade-in">
                <h2 className="text-5xl font-extrabold text-purple-800 mb-8 text-center leading-tight">On-Campus Dormitories</h2>
                <p className="text-xl text-gray-700 mb-10 text-center max-w-4xl mx-auto">
                  Experience vibrant campus life in our modern and comfortable dormitories. We offer a variety of living styles to suit your needs, fostering a supportive community.
                </p>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
                  {dormitoriesData.map(dorm => (
                    <div key={dorm.id} className="bg-purple-50 rounded-2xl shadow-lg overflow-hidden transform transition-all duration-300 hover:scale-105 hover:shadow-xl border border-purple-100">
                      <img
                        src={dorm.image}
                        alt={dorm.name}
                        className="w-full h-52 object-cover rounded-t-2xl"
                        onError={(e) => { e.target.onerror = null; e.target.src = "https://placehold.co/600x400/ADD8E6/000000?text=Image+Error"; }}
                      />
                      <div className="p-7">
                        <h3 className="text-3xl font-bold text-purple-700 mb-3">{dorm.name}</h3>
                        <p className="text-gray-600 mb-5 leading-relaxed">{dorm.description}</p>
                        <ul className="list-disc list-inside text-gray-600 mb-5 space-y-1">
                          {dorm.features.slice(0, 3).map((feature, index) => ( // Show first 3 features on card
                            <li key={index}>{feature}</li>
                          ))}
                          {dorm.features.length > 3 && <li>...and more!</li>}
                        </ul>
                        <button
                          onClick={() => handleViewDormDetails(dorm.id)}
                          className="w-full bg-purple-600 text-white py-3 rounded-lg font-bold text-lg hover:bg-purple-700 transition-colors duration-300 shadow-md hover:shadow-lg"
                        >
                          Explore {dorm.name}
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            </>
          )
        )}

        {/* Off-Campus Section */}
        {activeTab === 'off-campus' && (
          <section className="bg-white p-10 rounded-3xl shadow-2xl border border-fuchsia-200 animate-fade-in">
            <h2 className="text-5xl font-extrabold text-purple-800 mb-8 text-center leading-tight">Off-Campus Housing</h2>
            <p className="text-xl text-gray-700 mb-10 text-center max-w-4xl mx-auto">
              Explore various off-campus housing options near Evergreen University. Our resources can help you find the perfect place to call home.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
              {/* Off-Campus Card 1 */}
              <div className="bg-fuchsia-50 rounded-2xl shadow-lg overflow-hidden transform transition-all duration-300 hover:scale-105 hover:shadow-xl border border-fuchsia-100">
                <img
                  src="https://placehold.co/600x400/DDA0DD/000000?text=Apartments"
                  alt="Off-Campus Apartments"
                  className="w-full h-52 object-cover rounded-t-2xl"
                  onError={(e) => { e.target.onerror = null; e.target.src = "https://placehold.co/600x400/DDA0DD/000000?text=Image+Error"; }}
                />
                <div className="p-7">
                  <h3 className="text-3xl font-bold text-purple-700 mb-3">Local Apartments</h3>
                  <p className="text-gray-600 mb-5 leading-relaxed">
                    A curated list of popular apartment complexes within walking or biking distance, vetted for student convenience.
                  </p>
                  <button className="w-full bg-purple-600 text-white py-3 rounded-lg font-bold text-lg hover:bg-purple-700 transition-colors duration-300 shadow-md hover:shadow-lg">
                    View Listings
                  </button>
                </div>
              </div>

              {/* Off-Campus Card 2 */}
              <div className="bg-fuchsia-50 rounded-2xl shadow-lg overflow-hidden transform transition-all duration-300 hover:scale-105 hover:shadow-xl border border-fuchsia-100">
                <img
                  src="https://placehold.co/600x400/87CEEB/000000?text=Roommate+Finder"
                  alt="Roommate Finder"
                  className="w-full h-52 object-cover rounded-t-2xl"
                  onError={(e) => { e.target.onerror = null; e.target.src = "https://placehold.co/600x400/87CEEB/000000?text=Image+Error"; }}
                />
                <div className="p-7">
                  <h3 className="text-3xl font-bold text-purple-700 mb-3">Roommate Finder</h3>
                  <p className="text-gray-600 mb-5 leading-relaxed">
                    Connect with other Evergreen University students looking for compatible roommates.
                  </p>
                  <button className="w-full bg-purple-600 text-white py-3 rounded-lg font-bold text-lg hover:bg-purple-700 transition-colors duration-300 shadow-md hover:shadow-lg">
                    Find Roommates
                  </button>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* Resources Section */}
        {activeTab === 'resources' && (
          <section className="bg-white p-10 rounded-3xl shadow-2xl border border-purple-200 animate-fade-in">
            <h2 className="text-5xl font-extrabold text-purple-800 mb-8 text-center leading-tight">Housing Resources</h2>
            <p className="text-xl text-gray-700 mb-10 text-center max-w-4xl mx-auto">
              Helpful links and comprehensive guides to assist you with every step of your housing search and transition.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
              {/* Resource Card 1 */}
              <div className="bg-fuchsia-50 p-7 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105 hover:shadow-xl border border-fuchsia-100">
                <h3 className="text-3xl font-bold text-purple-700 mb-3">Housing Application</h3>
                <p className="text-gray-600 mb-5 leading-relaxed">
                  Access the official housing application portal for on-campus dorms and manage your application status.
                </p>
                <a href="#" className="text-fuchsia-600 hover:underline font-bold text-lg flex items-center">
                  Apply Now
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 ml-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                  </svg>
                </a>
              </div>

              {/* Resource Card 3 */}
              <div className="bg-fuchsia-50 p-7 rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-105 hover:shadow-xl border border-fuchsia-100">
                <h3 className="text-3xl font-bold text-purple-700 mb-3">Moving Checklist</h3>
                <p className="text-gray-600 mb-5 leading-relaxed">
                  A comprehensive checklist to help you prepare for your move, ensuring nothing is forgotten.
                </p>
                <a href="#" className="text-fuchsia-600 hover:underline font-bold text-lg flex items-center">
                  Get Checklist
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 ml-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                  </svg>
                </a>
              </div>
            </div>

            {/* Contact Form */}
            <div className="mt-16 p-10 bg-purple-50 rounded-3xl shadow-inner border border-purple-100">
              <h3 className="text-4xl font-bold text-purple-800 mb-8 text-center">Still Have Questions?</h3>
              <form onSubmit={handleSubmitInquiry} className="max-w-2xl mx-auto space-y-6">
                <div>
                  <label htmlFor="name" className="block text-gray-700 text-xl font-medium mb-2">Your Name</label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    required
                    className="w-full px-5 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-3 focus:ring-fuchsia-500 transition-all duration-200 text-lg shadow-sm"
                  />
                </div>
                <div>
                  <label htmlFor="email" className="block text-gray-700 text-xl font-medium mb-2">Your Email</label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    required
                    className="w-full px-5 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-3 focus:ring-fuchsia-500 transition-all duration-200 text-lg shadow-sm"
                  />
                </div>
                <div>
                  <label htmlFor="message" className="block text-gray-700 text-xl font-medium mb-2">Your Message</label>
                  <textarea
                    id="message"
                    name="message"
                    rows="6"
                    required
                    className="w-full px-5 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-3 focus:ring-fuchsia-500 transition-all duration-200 text-lg shadow-sm"
                  ></textarea>
                </div>
                <button
                  type="submit"
                  className="w-full bg-purple-600 text-white py-4 rounded-xl font-bold text-2xl hover:bg-purple-700 transition-colors duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
                >
                  Send Inquiry
                </button>
              </form>
              {formMessage && (
                <div className="mt-8 p-5 bg-green-100 text-green-800 rounded-xl text-center font-semibold text-lg shadow-md animate-fade-in">
                  {formMessage}
                </div>
              )}
            </div>
          </section>
        )}

        {/* Tech Support Section */}
        {activeTab === 'tech-support' && (
          <section className="bg-white p-10 rounded-3xl shadow-2xl border border-purple-200 animate-fade-in">
            <h2 className="text-5xl font-extrabold text-purple-800 mb-8 text-center leading-tight">Technical Support Request</h2>
            <p className="text-xl text-gray-700 mb-10 text-center max-w-4xl mx-auto">
              Experiencing technical issues with your devices? Fill out the form below, and our IT support team will assist you promptly.
            </p>

            <div className="mt-8 p-10 bg-purple-50 rounded-3xl shadow-inner border border-purple-100">
              <h3 className="text-4xl font-bold text-purple-800 mb-8 text-center">Submit a Support Ticket</h3>
              <form onSubmit={handleSubmitTechSupport} className="max-w-2xl mx-auto space-y-6">
                <div>
                  <label htmlFor="studentId" className="block text-gray-700 text-xl font-medium mb-2">Your Student ID</label>
                  <input
                    type="text"
                    id="studentId"
                    name="studentId"
                    required
                    className="w-full px-5 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-3 focus:ring-fuchsia-500 transition-all duration-200 text-lg shadow-sm"
                  />
                </div>
                <div>
                  <label htmlFor="techEmail" className="block text-gray-700 text-xl font-medium mb-2">Contact Email</label>
                  <input
                    type="email"
                    id="techEmail"
                    name="techEmail"
                    required
                    className="w-full px-5 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-3 focus:ring-fuchsia-500 transition-all duration-200 text-lg shadow-sm"
                  />
                </div>
                <div>
                  <label htmlFor="deviceType" className="block text-gray-700 text-xl font-medium mb-2">Device Type</label>
                  <select
                    id="deviceType"
                    name="deviceType"
                    required
                    className="w-full px-5 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-3 focus:ring-fuchsia-500 transition-all duration-200 text-lg shadow-sm bg-white"
                  >
                    <option value="">Select Device Type</option>
                    <option value="laptop">Laptop</option>
                    <option value="desktop">Desktop</option>
                    <option value="tablet">Tablet</option>
                    <option value="smartphone">Smartphone</option>
                    <option value="printer">Printer</option>
                    <option value="other">Other</option>
                  </select>
                </div>
                <div>
                  <label htmlFor="issueDescription" className="block text-gray-700 text-xl font-medium mb-2">Describe Your Issue</label>
                  <textarea
                    id="issueDescription"
                    name="issueDescription"
                    rows="6"
                    required
                    className="w-full px-5 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-3 focus:ring-fuchsia-500 transition-all duration-200 text-lg shadow-sm"
                  ></textarea>
                </div>
                <button
                  type="submit"
                  className="w-full bg-purple-600 text-white py-4 rounded-xl font-bold text-2xl hover:bg-purple-700 transition-colors duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
                >
                  Submit Request
                </button>
              </form>
              {techSupportMessage && (
                <div className="mt-8 p-5 bg-green-100 text-green-800 rounded-xl text-center font-semibold text-lg shadow-md animate-fade-in">
                  {techSupportMessage}
                </div>
              )}
            </div>
          </section>
        )}

        {/* Dining Hall Section */}
        {activeTab === 'dining-hall' && (
          <section className="bg-white p-10 rounded-3xl shadow-2xl border border-purple-200 animate-fade-in">
            <h2 className="text-5xl font-extrabold text-purple-800 mb-8 text-center leading-tight">Evergreen University Dining Hall</h2>
            <p className="text-xl text-gray-700 mb-10 text-center max-w-4xl mx-auto">
              Welcome to the Evergreen University Dining Hall, your culinary hub on campus! We offer a diverse range of delicious and nutritious options to fuel your academic journey.
            </p>

            <div className="flex flex-col md:flex-row gap-8 items-start">
              <img
                src="https://placehold.co/600x400/DDA0DD/000000?text=Dining+Hall" // Mauve placeholder
                alt="Evergreen University Dining Hall"
                className="w-full md:w-1/2 rounded-2xl shadow-xl object-cover h-80 md:h-auto"
                onError={(e) => { e.target.onerror = null; e.target.src = "https://placehold.co/600x400/CCCCCC/000000?text=Image+Not+Found"; }}
              />
              <div className="md:w-1/2">
                <p className="text-xl text-gray-700 mb-6 leading-relaxed">
                  Our dining hall is committed to providing a fresh, varied, and inclusive dining experience. From international cuisine to comfort food classics, there's something for everyone. We prioritize locally sourced ingredients and cater to various dietary needs.
                </p>
                <h3 className="text-3xl font-bold text-purple-700 mb-4">Features & Services:</h3>
                <ul className="list-disc list-inside text-gray-700 mb-6 text-lg space-y-2">
                  <li>Flexible Meal Plans</li>
                  <li>Vegetarian, Vegan, and Gluten-Free Options</li>
                  <li>Daily Rotating Menus</li>
                  <li>Grab-and-Go Station</li>
                  <li>Late-Night Dining Hours</li>
                  <li>Nutritional Information Available</li>
                  <li>Student Feedback Program</li>
                </ul>
                <button className="w-full bg-purple-600 text-white py-4 rounded-xl font-bold text-2xl hover:bg-purple-700 transition-colors duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
                  View Weekly Menu
                </button>
              </div>
            </div>
          </section>
        )}

        {/* Moving In Section */}
        {activeTab === 'moving-in' && (
          <section className="bg-white p-10 rounded-3xl shadow-2xl border border-purple-200 animate-fade-in">
            <h2 className="text-5xl font-extrabold text-purple-800 mb-8 text-center leading-tight">Moving In to Your Dorm</h2>
            <p className="text-xl text-gray-700 mb-10 text-center max-w-4xl mx-auto">
              Get ready for an exciting new chapter! Here's everything you need to know to make your move into Evergreen University dorms smooth and stress-free.
            </p>

            <div className="flex flex-col md:flex-row gap-8 items-start">
              <img
                src="https://placehold.co/600x400/D8BFD8/000000?text=Moving+In" // Mauve placeholder
                alt="Students moving into dorm"
                className="w-full md:w-1/2 rounded-2xl shadow-xl object-cover h-80 md:h-auto"
                onError={(e) => { e.target.onerror = null; e.target.src = "https://placehold.co/600x400/CCCCCC/000000?text=Image+Not+Found"; }}
              />
              <div className="md:w-1/2">
                <h3 className="text-3xl font-bold text-purple-700 mb-4">Key Dates & Information:</h3>
                <ul className="list-disc list-inside text-gray-700 mb-6 text-lg space-y-2">
                  <li>**Move-In Day:** August 20th, 2025 (9:00 AM - 5:00 PM)</li>
                  <li>**Early Arrival:** August 18th-19th (by request only)</li>
                  <li>**Orientation Week:** August 21st - 27th</li>
                  <li>**What to Bring:** Refer to the comprehensive checklist below.</li>
                  <li>**Parking:** Temporary parking available for unloading. Long-term permits available for purchase.</li>
                </ul>

                <h3 className="text-3xl font-bold text-purple-700 mb-4 mt-8">Moving Checklist:</h3>
                <ul className="list-disc list-inside text-gray-700 mb-6 text-lg space-y-2">
                  <li>Bedding (sheets, comforter, pillows)</li>
                  <li>Toiletries & Towels</li>
                  <li>Desk lamp & School Supplies</li>
                  <li>Clothes & Hangers</li>
                  <li>Small first-aid kit</li>
                  <li>Power strip with surge protector</li>
                  <li>Reusable water bottle & coffee mug</li>
                  <li>Personal electronics (laptop, phone, chargers)</li>
                  <li>Decorations to personalize your space</li>
                </ul>
                <button
                  type="button" // Changed to type="button" as it's not a form submission
                  className="w-full bg-purple-600 text-white py-4 rounded-xl font-bold text-2xl hover:bg-purple-700 transition-colors duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
                >
                  Download Full Checklist
                </button>
              </div>
            </div>
          </section>
        )}

        {/* FAQ Section */}
        {activeTab === 'faq' && <FAQPage />}

        {/* On-Campus Jobs Section */}
        {activeTab === 'on-campus-jobs' && (
          <section className="bg-white p-10 rounded-3xl shadow-2xl border border-purple-200 animate-fade-in">
            <h2 className="text-5xl font-extrabold text-purple-800 mb-8 text-center leading-tight">On-Campus Jobs for Students</h2>
            <p className="text-xl text-gray-700 mb-10 text-center max-w-4xl mx-auto">
              Looking to earn money and gain valuable experience while studying? Evergreen University offers a variety of on-campus job opportunities designed to fit around your academic schedule.
            </p>

            <div className="flex flex-col md:flex-row gap-8 items-start">
              <img
                src="https://placehold.co/600x400/D8BFD8/000000?text=On-Campus+Jobs"
                alt="Students working on campus"
                className="w-full md:w-1/2 rounded-2xl shadow-xl object-cover h-80 md:h-auto"
                onError={(e) => { e.target.onerror = null; e.target.src = "https://placehold.co/600x400/CCCCCC/000000?text=Image+Not+Found"; }}
              />
              <div className="md:w-1/2">
                <h3 className="text-3xl font-bold text-purple-700 mb-4">Why Work On-Campus?</h3>
                <ul className="list-disc list-inside text-gray-700 mb-6 text-lg space-y-2">
                  <li>**Flexible Hours:** Most positions offer schedules that accommodate your classes and study time.</li>
                  <li>**Convenient Location:** Work right on campus, saving commute time.</li>
                  <li>**Skill Development:** Gain professional skills relevant to your studies or future career.</li>
                  <li>**Networking:** Connect with faculty, staff, and other students.</li>
                  <li>**Financial Aid:** Many positions are part of work-study programs.</li>
                </ul>

                <h3 className="text-3xl font-bold text-purple-700 mb-4 mt-8">Types of On-Campus Jobs:</h3>
                <ul className="list-disc list-inside text-gray-700 mb-6 text-lg space-y-2">
                  <li>Library Assistant</li>
                  <li>Dining Hall Staff</li>
                  <li>Lab Assistant</li>
                  <li>Office Assistant (various departments)</li>
                  <li>Resident Advisor (RA)</li>
                  <li>Tutoring Services</li>
                  <li>Campus Tour Guide</li>
                  <li>Event Staff</li>
                </ul>
                <button
                  type="button" // Changed to type="button" as it's not a form submission
                  className="w-full bg-purple-600 text-white py-4 rounded-xl font-bold text-2xl hover:bg-purple-700 transition-colors duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
                >
                  View Job Openings
                </button>
              </div>
            </div>
          </section>
        )}

        {/* About Us Section */}
        {activeTab === 'about-us' && <AboutUsPage />}
      </main>

      {/* Footer Section */}
      <footer className="bg-fuchsia-900 text-white py-8 px-6 md:px-12 rounded-t-3xl mt-16 shadow-inner">
        <div className="container mx-auto grid grid-cols-1 md:grid-cols-3 gap-8 text-center md:text-left">
          <div>
            <h3 className="text-2xl font-bold mb-4 text-fuchsia-200">Quick Links</h3>
            <ul className="space-y-2">
              <li><a href="#" className="hover:underline text-lg">Admissions</a></li>
              <li><a href="#" className="hover:underline text-lg">Academics</a></li>
              <li><a href="#" className="hover:underline text-lg">Student Life</a></li>
              <li><a href="#" className="hover:underline text-lg">Campus Map</a></li>
              <li><a href="#" className="hover:underline text-lg">Directory</a></li>
            </ul>
          </div>
          <div>
            <h3 className="text-2xl font-bold mb-4 text-fuchsia-200">Contact Us</h3>
            <p className="text-lg">123 University Ave, Fictional City, FC 12345</p>
            <p className="text-lg">Phone: (123) 456-7890</p>
            <p className="text-lg">Email: info@evergreen.edu</p>
            <div className="flex justify-center md:justify-start space-x-4 mt-4">
              {/* Social Media Icons - Placeholder SVGs */}
              <a href="#" aria-label="Facebook" className="text-white hover:text-fuchsia-300 transition-colors duration-300">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M9 8h-3v4h3v12h5v-12h3.642l.358-4h-4v-1.667c0-.955.192-1.333 1.115-1.333h2.885v-5h-3.812c-3.233 0-4.188 1.508-4.188 4.035v2.965z"/></svg>
              </a>
              <a href="#" aria-label="Twitter" className="text-white hover:text-fuchsia-300 transition-colors duration-300">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.594 0-6.494 2.902-6.494 6.492 0 .509.058 1.006.171 1.486-5.392-.27-10.17-2.868-13.39-6.836-.562.961-.886 2.083-.886 3.283 0 2.272 1.159 4.288 2.919 5.464-.859-.026-1.66-.263-2.365-.656v.083c0 3.142 2.237 5.764 5.204 6.363-.544.148-1.119.225-1.703.225-.417 0-.82-.041-1.215-.116.827 2.574 3.22 4.44 6.062 4.44 0-.001 0-.001 0-.002 0 .001 0 .001 0 .002-2.217 1.642-4.99 2.62-7.985 2.62-1.954 0-3.813-.114-5.597-.325 2.869 1.849 6.273 2.927 9.95 2.927 11.933 0 18.44-9.877 18.44-18.44 0-.281-.007-.562-.02-.843.987-.714 1.846-1.607 2.531-2.617z"/></svg>
              </a>
              <a href="#" aria-label="Instagram" className="text-white hover:text-fuchsia-300 transition-colors duration-300">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.07 1.645.07 4.85s-.012 3.584-.07 4.85c-.149 3.225-1.691 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07s-3.584-.012-4.85-.07c-3.225-.148-4.771-1.691-4.919-4.919-.058-1.265-.07-1.644-.07-4.85s.012-3.584.07-4.85c.148-3.227 1.691-4.773 4.919-4.919 1.266-.057 1.645-.069 4.85-.069zm0-2.163c-3.63 0-4.06.016-5.483.076-3.77 0-6.173 2.398-6.234 6.234-.06 1.423-.076 1.853-.076 5.484s.016 4.06.076 5.484c.061 3.836 2.464 6.234 6.234 6.234 1.423.06 1.853.076 5.484.076s4.06-.016 5.484-.076c3.77-.061 6.173-2.464 6.234-6.234.06-1.423.076-1.853.076-5.484s-.016-4.06-.076-5.484c-.061-3.77-2.464-6.173-6.234-6.234-1.423-.06-1.853-.076-5.484-.076zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.162 6.162 6.162 6.162-2.759 6.162-6.162c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.791-4-4s1.791-4 4-4 4 1.791 4 4-1.791 4-4 4zm6.406-11.845c-.796 0-1.44-.644-1.44-1.44s.644-1.44 1.44-1.44 1.44.644 1.44 1.44-.644 1.44-1.44 1.44z"/></svg>
              </a>
            </div>
          </div>
          <div>
            <h3 className="text-2xl font-bold mb-4 text-fuchsia-200">Connect With Us</h3>
            <ul className="space-y-2">
              <li><a href="#" className="hover:underline text-lg">Alumni</a></li>
              <li><a href="#" className="hover:underline text-lg">Giving</a></li>
              <li><a href="#" className="hover:underline text-lg">Careers at EU</a></li>
              <li><a href="#" className="hover:underline text-lg">News & Events</a></li>
            </ul>
          </div>
        </div>
        <div className="border-t border-fuchsia-800 mt-8 pt-6 text-md opacity-80">
          <p>&copy; {new Date().getFullYear()} Evergreen University. All rights reserved. | <a href="#" className="hover:underline">Privacy Policy</a> | <a href="#" className="hover:underline">Terms of Use</a></p>
        </div>
      </footer>

      {/* Tailwind CSS CDN and custom styles for animations */}
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        body {
          font-family: 'Inter', sans-serif;
        }
        .animate-fade-in {
          animation: fadeIn 0.8s ease-out;
        }
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  );
};

export default App;
