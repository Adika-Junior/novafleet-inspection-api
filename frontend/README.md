# NovaFleet Inspection Tracker - Frontend

A modern, responsive web interface for the NovaFleet Vehicle Inspection API.

## 🚀 Quick Setup

### Prerequisites
- Backend API running on http://localhost:8000
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Start Frontend Server
```bash
# Navigate to frontend directory
cd frontend

# Start HTTP server (NO virtual environment needed)
python -m http.server 3000
```

### Access the Application
- **Basic Version**: http://localhost:3000/index.html
- **Advanced Version**: http://localhost:3000/index-advanced.html

## 📋 Available Versions

### Basic Version (`index.html`)
**Features:**
- Dashboard with statistics cards
- Add new inspections with form validation
- View all inspections in a table
- Edit and delete inspections
- Search by vehicle plate
- Responsive design

**Perfect for:** Simple inspection management

### Advanced Version (`index-advanced.html`)
**All basic features PLUS:**
- Real-time search with debouncing
- Data export (CSV/JSON)
- Advanced statistics modal
- Offline support with auto-sync
- Enhanced UI components
- Online/offline status indicator

**Perfect for:** Power users and advanced workflows

## 🔍 Search Functionality

Both versions include vehicle plate search:

### How to Search
1. **Type in search box**: Results filter in real-time
2. **Partial matching**: "ABC" finds "ABC-1234", "DEF-ABC", etc.
3. **Case insensitive**: Works with any case
4. **Clear search**: Click "Clear" button to show all

### Search Features
- **Debounced input**: 300ms delay prevents excessive filtering
- **Visual feedback**: Shows search results count
- **No results handling**: Clear message when no matches found
- **Instant reset**: One-click to clear search

## 🎨 Features Overview

### Dashboard Statistics
- **Total Inspections**: Count of all inspections
- **Scheduled**: Inspections with "scheduled" status  
- **Passed**: Inspections with "passed" status
- **Failed**: Inspections with "failed" status
- **Real-time updates**: Statistics update after any changes

### Inspection Management
- **Add New**: Form with validation and date restrictions
- **View All**: Sortable table with all inspection data
- **Edit**: Modal-based editing with pre-filled data
- **Delete**: Confirmation-based deletion
- **Search**: Real-time filtering by vehicle plate

### User Experience
- **Success/Error Messages**: Clear feedback for all operations
- **Loading States**: Spinners during API calls
- **Form Validation**: Client-side validation with helpful messages
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Professional UI**: Bootstrap 5 with custom styling

## 🔧 Technical Details

### Technology Stack
- **HTML5**: Semantic markup
- **CSS3**: Custom styles with Bootstrap 5
- **JavaScript (ES6+)**: Modern JavaScript with async/await
- **Bootstrap 5**: Responsive framework
- **Font Awesome 6**: Icons
- **Fetch API**: HTTP requests to backend

### Browser Support
- **Chrome**: 60+
- **Firefox**: 55+  
- **Safari**: 12+
- **Edge**: 79+

### File Structure
```
frontend/
├── index.html                  # Basic version - simple search
├── index-advanced.html         # Advanced version - with exports  
├── script.js                   # Core functionality + search
├── advanced-features.js        # Export, statistics, offline
├── styles.css                  # Custom styling
├── README.md                   # Frontend documentation
└── *.md                        # Additional guides
```

## 🌐 API Integration

### Endpoints Used
- `GET /api/inspections` - List all inspections
- `POST /api/inspections` - Create new inspection  
- `GET /api/inspections/{id}` - Get single inspection
- `PUT /api/inspections/{id}` - Update inspection
- `DELETE /api/inspections/{id}` - Delete inspection

### Error Handling
- **Network errors**: User-friendly connection messages
- **Validation errors**: Field-specific error display
- **API errors**: Proper HTTP status code handling
- **Offline support**: Queue operations when offline (advanced version)

## 🧪 Testing the Frontend

### Basic Testing
1. **Load Dashboard**: Statistics should display
2. **Add Inspection**: Fill form and submit
3. **Search**: Type vehicle plate in search box
4. **Edit**: Click edit button, modify data, save
5. **Delete**: Click delete button, confirm

### Advanced Testing (Advanced Version Only)
1. **Export Data**: Click CSV/JSON export buttons
2. **View Statistics**: Click Statistics button
3. **Offline Mode**: Disconnect internet, try operations
4. **Auto-sync**: Reconnect internet, verify sync

### Search Testing
1. **Type "ABC"**: Should filter to plates containing "ABC"
2. **Clear search**: Click Clear button, should show all
3. **No results**: Search for non-existent plate
4. **Case insensitive**: Try "abc", "ABC", "Abc"

## 🔧 Troubleshooting

### Common Issues

**1. Frontend not loading data**
- Check backend is running: http://localhost:8000/api/inspections
- Check browser console (F12) for errors
- Verify CORS is configured in Django

**2. Search not working**
- Refresh the page
- Check browser console for JavaScript errors
- Ensure you're using the correct version (basic vs advanced)

**3. Export buttons not working (Advanced version)**
- Check browser allows downloads
- Ensure there's data to export
- Try different browser

**4. Styling issues**
- Clear browser cache (Ctrl+F5)
- Check internet connection (Bootstrap/FontAwesome CDN)
- Verify all CSS files are loading

### Debug Steps
1. **Open Developer Tools** (F12)
2. **Check Console tab** for JavaScript errors
3. **Check Network tab** for failed requests
4. **Verify API responses** in Network tab

## 🚀 Deployment

### Development
- Use `python -m http.server 3000` for local testing
- No build process required
- All dependencies loaded from CDN

### Production
- Upload files to web server (Apache, Nginx)
- Update API_BASE_URL in script.js for production API
- Consider using a CDN for static assets
- Enable gzip compression for better performance

### Example Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/frontend;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Enable gzip compression
    gzip on;
    gzip_types text/css application/javascript;
}
```

## 🔒 Security

### Client-Side Security
- **Input validation**: Prevents XSS attacks
- **No sensitive data**: All data comes from API
- **CORS compliance**: Respects browser security policies
- **Safe HTML rendering**: Proper escaping of user content

### Best Practices
- Always validate data on server side
- Use HTTPS in production
- Implement proper authentication (future enhancement)
- Regular security updates for dependencies

## 📱 Mobile Support

### Responsive Features
- **Mobile-first design**: Optimized for small screens
- **Touch-friendly**: Large buttons and touch targets
- **Responsive tables**: Horizontal scrolling on mobile
- **Collapsible navigation**: Better mobile UX

### Mobile Testing
- Test on actual devices when possible
- Use browser developer tools device simulation
- Verify touch interactions work properly
- Check performance on slower connections

## 🔮 Future Enhancements

### Planned Features
- **Bulk operations**: Select multiple inspections
- **Advanced filtering**: Date ranges, status combinations
- **Print reports**: PDF generation
- **Real-time updates**: WebSocket integration
- **User preferences**: Save search settings
- **Themes**: Dark/light mode toggle

### Technical Improvements
- **Progressive Web App**: Offline-first approach
- **Service Worker**: Better caching and offline support
- **Performance**: Lazy loading and code splitting
- **Accessibility**: WCAG compliance improvements

## 📞 Support

### Getting Help
- Check this README for common issues
- Review browser console for error messages
- Verify backend API is working: http://localhost:8000/swagger/
- Test with different browsers

### Reporting Issues
When reporting issues, include:
- Browser and version
- Steps to reproduce
- Error messages from console
- Screenshots if applicable

---

**The NovaFleet frontend provides a complete, professional interface for vehicle inspection management with modern web technologies and excellent user experience.**