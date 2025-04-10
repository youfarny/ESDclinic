// src/services/zoomApi.js

// For demo purposes, we'll use hardcoded values matching your personal Zoom account
const ZOOM_PERSONAL_MEETING_ID = "3724875036" // Removed spaces for direct API use
const ZOOM_JOIN_URL = "https://us04web.zoom.us/j/3724875036?pwd=eXMzSnpuR2I4OUZyYkVBbWxlZ2E0UT09"
const ZOOM_PASSWORD = "eXMzSnpuR2I4OUZyYkVBbWxlZ2E0UT09"

// Create a new Zoom meeting
const createZoomMeeting = async (appointmentData) => {
  try {
    // For demo purposes, return hardcoded values instead of making an API call
    // In production, you would make an actual API call to Zoom
    
    const patientName = appointmentData.patientName || 'Patient'
    const appointmentId = appointmentData.id || 'Unknown'
    
    return {
      id: ZOOM_PERSONAL_MEETING_ID,
      password: ZOOM_PASSWORD,
      join_url: ZOOM_JOIN_URL,
      topic: `Medical Consultation - ${patientName} (ID: ${appointmentId})`,
      duration: 30,
      start_time: new Date().toISOString()
    }
  } catch (error) {
    console.error('Failed to create Zoom meeting:', error)
    throw error
  }
}

// Get information about an existing Zoom meeting
const getZoomMeeting = async (meetingId) => {
  try {
    // For demo purposes, return hardcoded values
    return {
      id: ZOOM_PERSONAL_MEETING_ID,
      password: ZOOM_PASSWORD,
      join_url: ZOOM_JOIN_URL,
      topic: 'Medical Consultation',
      duration: 30,
      start_time: new Date().toISOString()
    }
  } catch (error) {
    console.error('Failed to get Zoom meeting:', error)
    throw error
  }
}

// Delete an existing Zoom meeting (not needed for demo but included for completeness)
const deleteZoomMeeting = async (meetingId) => {
  try {
    // For demo, just return success without actually deleting
    return { success: true }
  } catch (error) {
    console.error('Failed to delete Zoom meeting:', error)
    throw error
  }
}

export const zoomApi = {
  createZoomMeeting,
  getZoomMeeting,
  deleteZoomMeeting
}