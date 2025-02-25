// Initialize Lucide icons
document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
});

// Sample data for groups - now with 6 items each
const currentGroups = [
    {
        id: 1,
        name: 'ISTM 631 Group A',
        members: 25,
        faculty: 'Dr. Sarah Martinez',
        lastActive: '2 hours ago'
    },
    {
        id: 2,
        name: 'ISTM 615 Group B',
        members: 30,
        faculty: 'Dr. James Wilson',
        lastActive: '4 hours ago'
    },
    {
        id: 3,
        name: 'ISTM 645 Group C',
        members: 28,
        faculty: 'Dr. Emily Chen',
        lastActive: '1 day ago'
    },
    {
        id: 4,
        name: 'ISTM 631 Group D',
        members: 27,
        faculty: 'Dr. Michael Brown',
        lastActive: '3 hours ago'
    },
    {
        id: 5,
        name: 'ISTM 615 Group E',
        members: 29,
        faculty: 'Dr. Lisa Anderson',
        lastActive: '5 hours ago'
    },
    {
        id: 6,
        name: 'ISTM 645 Group F',
        members: 26,
        faculty: 'Dr. Robert Taylor',
        lastActive: '2 days ago'
    }
];

const previousGroups = [
    {
        id: 7,
        name: 'ISTM 631 Fall 2023',
        members: 25,
        faculty: 'Dr. Sarah Martinez',
        lastActive: '3 months ago'
    },
    {
        id: 8,
        name: 'ISTM 615 Fall 2023',
        members: 30,
        faculty: 'Dr. James Wilson',
        lastActive: '3 months ago'
    },
    {
        id: 9,
        name: 'ISTM 645 Fall 2023',
        members: 28,
        faculty: 'Dr. Emily Chen',
        lastActive: '3 months ago'
    },
    {
        id: 10,
        name: 'ISTM 631 Summer 2023',
        members: 24,
        faculty: 'Dr. Michael Brown',
        lastActive: '6 months ago'
    },
    {
        id: 11,
        name: 'ISTM 615 Summer 2023',
        members: 29,
        faculty: 'Dr. Lisa Anderson',
        lastActive: '6 months ago'
    },
    {
        id: 12,
        name: 'ISTM 645 Summer 2023',
        members: 27,
        faculty: 'Dr. Robert Taylor',
        lastActive: '6 months ago'
    }
];

// Function to create a card element
function createCard(group) {
    const card = document.createElement('div');
    card.className = 'card';
    card.setAttribute('data-id', group.id);
    
    card.innerHTML = `
        <h3>${group.name}</h3>
        <div class="card-info">
            <p>Members: <span>${group.members}</span></p>
            <p>Faculty: <span>${group.faculty}</span></p>
            <p>Last Active: <span>${group.lastActive}</span></p>
        </div>
    `;
    
    card.addEventListener('click', () => handleCardClick(group));
    
    return card;
}

// Function to handle card clicks
function handleCardClick(group) {
    console.log(`Clicked group: ${group.name}`);
}

// Function to handle scrolling
function initializeScroll(section) {
    const container = section.querySelector('.cards-container');
    const leftBtn = section.querySelector('.scroll-btn.left');
    const rightBtn = section.querySelector('.scroll-btn.right');
    const scrollAmount = 330; // card width + gap

    leftBtn.addEventListener('click', () => {
        container.style.transform = `translateX(${Math.min(0, parseInt(container.style.transform?.slice(11) || 0) + scrollAmount)}px)`;
        updateScrollButtons(section);
    });

    rightBtn.addEventListener('click', () => {
        const maxScroll = -(container.scrollWidth - container.parentElement.clientWidth);
        container.style.transform = `translateX(${Math.max(maxScroll, parseInt(container.style.transform?.slice(11) || 0) - scrollAmount)}px)`;
        updateScrollButtons(section);
    });

    // Initial button state
    updateScrollButtons(section);
}

function updateScrollButtons(section) {
    const container = section.querySelector
}