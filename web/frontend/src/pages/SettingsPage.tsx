import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Settings, Bell, Shield, Palette, Globe, User, Moon, Sun } from 'lucide-react'
import toast from 'react-hot-toast'

const SettingsPage: React.FC = () => {
  const [darkMode, setDarkMode] = useState(true)
  const [notifications, setNotifications] = useState(true)
  const [emailUpdates, setEmailUpdates] = useState(false)

  const handleSaveSettings = () => {
    toast.success('Settings saved successfully!')
  }

  const settingsSections = [
    {
      title: 'Appearance',
      icon: Palette,
      settings: [
        {
          label: 'Dark Mode',
          description: 'Use dark theme for the application',
          type: 'toggle',
          value: darkMode,
          onChange: setDarkMode,
        },
      ],
    },
    {
      title: 'Notifications',
      icon: Bell,
      settings: [
        {
          label: 'Push Notifications',
          description: 'Receive notifications for new recommendations',
          type: 'toggle',
          value: notifications,
          onChange: setNotifications,
        },
        {
          label: 'Email Updates',
          description: 'Receive weekly movie recommendations via email',
          type: 'toggle',
          value: emailUpdates,
          onChange: setEmailUpdates,
        },
      ],
    },
    {
      title: 'Privacy',
      icon: Shield,
      settings: [
        {
          label: 'Public Profile',
          description: 'Allow others to see your watch history',
          type: 'toggle',
          value: false,
          onChange: () => {},
        },
        {
          label: 'Data Collection',
          description: 'Help improve recommendations by sharing usage data',
          type: 'toggle',
          value: true,
          onChange: () => {},
        },
      ],
    },
    {
      title: 'Preferences',
      icon: User,
      settings: [
        {
          label: 'Language',
          description: 'Choose your preferred language',
          type: 'select',
          value: 'English',
          options: ['English', 'Spanish', 'French', 'German'],
        },
        {
          label: 'Region',
          description: 'Set your region for localized content',
          type: 'select',
          value: 'United States',
          options: ['United States', 'United Kingdom', 'Canada', 'Australia'],
        },
      ],
    },
  ]

  return (
    <div className="min-h-screen gradient-bg py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold mb-4 flex items-center gap-3">
            <Settings size={32} />
            Settings
          </h1>
          <p className="text-white/60">Customize your MoviePicker experience</p>
        </motion.div>

        {/* Settings Sections */}
        <div className="space-y-6">
          {settingsSections.map((section, sectionIndex) => (
            <motion.div
              key={section.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: sectionIndex * 0.1 }}
              className="glass-effect p-6 rounded-lg"
            >
              <div className="flex items-center gap-3 mb-6">
                <section.icon size={24} className="text-primary-500" />
                <h2 className="text-xl font-semibold">{section.title}</h2>
              </div>

              <div className="space-y-4">
                {section.settings.map((setting, settingIndex) => (
                  <div
                    key={setting.label}
                    className="flex items-center justify-between p-4 bg-white/5 rounded-lg"
                  >
                    <div className="flex-1">
                      <h3 className="font-medium mb-1">{setting.label}</h3>
                      <p className="text-white/60 text-sm">{setting.description}</p>
                    </div>

                    {setting.type === 'toggle' && (
                      <button
                        onClick={() => setting.onChange(!setting.value)}
                        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                          setting.value ? 'bg-primary-500' : 'bg-white/20'
                        }`}
                      >
                        <span
                          className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                            setting.value ? 'translate-x-6' : 'translate-x-1'
                          }`}
                        />
                      </button>
                    )}

                    {setting.type === 'select' && (
                      <select
                        value={setting.value}
                        onChange={(e) => {
                          // Handle select change
                        }}
                        className="bg-movie-light border border-white/20 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                      >
                        {setting.options?.map((option) => (
                          <option key={option} value={option}>
                            {option}
                          </option>
                        ))}
                      </select>
                    )}
                  </div>
                ))}
              </div>
            </motion.div>
          ))}
        </div>

        {/* Save Button */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="mt-8 flex justify-end"
        >
          <button
            onClick={handleSaveSettings}
            className="btn-primary px-8 py-3 text-lg"
          >
            Save Settings
          </button>
        </motion.div>

        {/* Additional Options */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mt-8 space-y-4"
        >
          <div className="glass-effect p-6 rounded-lg">
            <h3 className="text-lg font-semibold mb-4">Account Actions</h3>
            <div className="space-y-3">
              <button className="w-full text-left p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-colors">
                Export My Data
              </button>
              <button className="w-full text-left p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-colors">
                Delete Account
              </button>
              <button className="w-full text-left p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-colors">
                Privacy Policy
              </button>
              <button className="w-full text-left p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-colors">
                Terms of Service
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default SettingsPage 